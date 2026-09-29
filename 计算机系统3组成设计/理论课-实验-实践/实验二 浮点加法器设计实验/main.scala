import chisel3._
import chisel3.util._

class FP32Adder extends Module {

  val io = IO(new Bundle {
    val a = Input(UInt(32.W))
    val b = Input(UInt(32.W))
    val y = Output(UInt(32.W))
  })

  // ============================================================
  // 1. IEEE-754 字段拆分
  // ============================================================

  val signA = io.a(31)
  val expA  = io.a(30, 23)
  val fracA = io.a(22, 0)

  val signB = io.b(31)
  val expB  = io.b(30, 23)
  val fracB = io.b(22, 0)

  // ============================================================
  // 特殊值判断
  // ============================================================

  val isZeroA = (expA === 0.U) && (fracA === 0.U)
  val isZeroB = (expB === 0.U) && (fracB === 0.U)

  val isInfA = (expA === 255.U) && (fracA === 0.U)
  val isInfB = (expB === 255.U) && (fracB === 0.U)

  val isNaNA = (expA === 255.U) && (fracA =/= 0.U)
  val isNaNB = (expB === 255.U) && (fracB =/= 0.U)

  // ============================================================
  // 2. 恢复隐藏位
  // ============================================================

  val hiddenA = Mux(expA === 0.U, 0.U(1.W), 1.U(1.W))
  val hiddenB = Mux(expB === 0.U, 0.U(1.W), 1.U(1.W))

  val sigA = Cat(hiddenA, fracA)     // 24 bit 有效尾数
  val sigB = Cat(hiddenB, fracB)     // 24 bit 有效位数

  // subnormal 的有效指数看成 1
  val expEffA = Mux(expA === 0.U, 1.U(8.W), expA)
  val expEffB = Mux(expB === 0.U, 1.U(8.W), expB)
  val sigExtA = Cat(sigA, 0.U(3.W))
  val sigExtB = Cat(sigB, 0.U(3.W))

  // ============================================================
  // 3. 比较两个数的绝对值
  // ============================================================

  val aGreater =
    (expEffA > expEffB) ||
    ((expEffA === expEffB) && (sigA >= sigB))

  val bigSign = Mux(aGreater, signA, signB)
  val smallSign = Mux(aGreater, signB, signA)

  val bigExp = Mux(aGreater, expEffA, expEffB)
  val smallExp = Mux(aGreater, expEffB, expEffA)

  val bigSig = Mux(aGreater, sigExtA, sigExtB)
  val smallSig = Mux(aGreater, sigExtB, sigExtA)

  // ============================================================
  // 4. 阶码求差
  // ============================================================

  val expDiff = bigExp - smallExp

  // ============================================================
  // 5. 小数右移实现对阶
  // ============================================================

  def shiftRightJam(x: UInt, dist: UInt): UInt = {

    val width = 27

    val choices = Wire(Vec(width + 1, UInt(width.W)))

    // 不移动
    choices(0) := x

    // 移动 1 ~ 26 位
    for (i <- 1 until width) {

      val shifted = (x >> i).pad(width)

      val sticky = x(i - 1, 0).orR

      choices(i) :=
        Cat(
          shifted(width - 1, 1),
          shifted(0) | sticky
        )
    }

    // 移动 >= 27 位以后，
    // 只剩 sticky 信息
    choices(width) :=
      Mux(
        x.orR,
        1.U(width.W),
        0.U(width.W)
      )

    val index =
      Mux(
        dist >= width.U,
        width.U,
        dist
      )

    choices(index)
  }

  val smallAligned =
    shiftRightJam(smallSig, expDiff)

  // ============================================================
  // 6. 尾数加/减
  // ============================================================

  val sameSign = bigSign === smallSign

  // +& 保留额外的 carry bit
  val addResult = bigSig +& smallAligned

  val subResult = bigSig - smallAligned

  val rawIsZero =
    (!sameSign) && (subResult === 0.U)

  // ============================================================
  // 7.1 加法情况下规格化
  // ============================================================

  val addNormSig = Wire(UInt(27.W))
  val addNormExp = Wire(UInt(9.W))

  when(addResult(27)) {
    addNormSig :=
      Cat(
        addResult(27, 2),
        addResult(1) | addResult(0)
      )

    addNormExp :=
      bigExp +& 1.U

  }.otherwise {

    addNormSig := addResult(26, 0)

    addNormExp :=
      Cat(0.U(1.W), bigExp)
  }

  // ============================================================
  // 7.2 减法情况下规格化
  // ============================================================

  val leadingZeros =
    PriorityEncoder(Reverse(subResult))

  val subNormSig = Wire(UInt(27.W))
  val subNormExp = Wire(UInt(9.W))
  val subUnderflow = Wire(Bool())

  subUnderflow :=
    leadingZeros >= bigExp

  subNormSig :=
    subResult << leadingZeros

  subNormExp :=
    Cat(0.U(1.W), bigExp) - leadingZeros

  // ============================================================
  // 根据加法/减法选择规格化结果
  // ============================================================

  val normSig = Wire(UInt(27.W))
  val normExp = Wire(UInt(9.W))

  when(sameSign) {

    normSig := addNormSig
    normExp := addNormExp

  }.otherwise {

    normSig := subNormSig
    normExp := subNormExp
  }

  // ============================================================
  // 8.1 IEEE-754 舍入
  // ============================================================

  val significand = normSig(26, 3)

  val guardBit  = normSig(2)
  val roundBit  = normSig(1)
  val stickyBit = normSig(0)

  val lsb = significand(0)
  val roundUp =
    guardBit &&
      (roundBit || stickyBit || lsb)

  // 多留一位检查舍入进位
  val rounded =
    significand +& roundUp.asUInt

  // ============================================================
  // 8.2 舍入后可能再次产生进位
  // ============================================================

  val finalSig = Wire(UInt(24.W))
  val finalExp = Wire(UInt(9.W))

  when(rounded(24)) {

    finalSig := rounded(24, 1)
    finalExp := normExp + 1.U

  }.otherwise {

    finalSig := rounded(23, 0)
    finalExp := normExp
  }

  // ============================================================
  // 9. 重新组合 sign / exponent / fraction
  // ============================================================

  val resultNormal =
    Cat(
      bigSign,
      finalExp(7, 0),
      finalSig(22, 0)
    )
  val positiveZero =
    0.U(32.W)

  val infinity =
    Cat(
      bigSign,
      "hFF".U(8.W),
      0.U(23.W)
    )
  val qNaN =
    "h7FC00000".U(32.W)

  // ============================================================
  // 10. 特殊情况
  // ============================================================
  val result = Wire(UInt(32.W))
  result := resultNormal
  when(isNaNA || isNaNB) {

    result := qNaN
  }.elsewhen(
    isInfA &&
    isInfB &&
    (signA =/= signB)
  ) {

    result := qNaN

  }.elsewhen(isInfA) {

    result := io.a

  }.elsewhen(isInfB) {

    result := io.b

  // 0 + B
  }.elsewhen(isZeroA) {

    result := io.b

  // A + 0
  }.elsewhen(isZeroB) {

    result := io.a

  // 完全抵消
  }.elsewhen(rawIsZero) {

    result := positiveZero
  }.elsewhen(
    (!sameSign) && subUnderflow
  ) {

    result := positiveZero
  }.elsewhen(finalExp >= 255.U) {

    result := infinity
  }

  io.y := result
}
