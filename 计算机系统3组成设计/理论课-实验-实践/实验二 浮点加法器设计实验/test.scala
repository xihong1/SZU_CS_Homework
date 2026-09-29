import chisel3._
import chiseltest._
import org.scalatest.flatspec.AnyFlatSpec

class FP32AdderTest extends AnyFlatSpec with ChiselScalatestTester {

  behavior of "FP32Adder Task1"

  def floatBits(x: Float): BigInt = {
    BigInt(java.lang.Float.floatToRawIntBits(x) & 0xffffffffL)
  }

  def hex32(x: BigInt): String = {
    f"0x${x.longValue}%08X"
  }

  it should "show fields of 1.5 and 2.25" in {
    test(new FP32Adder)
      .withAnnotations(Seq(WriteVcdAnnotation)) { c =>

        val a = 1.5f
        val b = 2.25f

        val aBits = floatBits(a)
        val bBits = floatBits(b)

        c.io.a.poke(aBits.U)
        c.io.b.poke(bBits.U)
        c.clock.step()

        println("========================================")
        println("Task 1 : Field split & significand restore")
        println("----------------------------------------")
        println(s"A = $a   bits = ${hex32(aBits)}")
        println(s"B = $b   bits = ${hex32(bBits)}")
        println("----------------------------------------")
        println("A: sign=0  exp=127 (0x7F)  frac=0x400000  sig=0xC00000")
        println("B: sign=0  exp=128 (0x80)  frac=0x100000  sig=0x900000")
        println("========================================")

        // ===== 用 Scala 端算出的字段做断言 =====
        // A = 1.5 = 0x3FC00000
        val aSign = (aBits >> 31) & 0x1
        val aExp  = (aBits >> 23) & 0xFF
        val aFrac = aBits & 0x7FFFFF
        val aSig  = (BigInt(1) << 23) | aFrac

        // B = 2.25 = 0x40100000
        val bSign = (bBits >> 31) & 0x1
        val bExp  = (bBits >> 23) & 0xFF
        val bFrac = bBits & 0x7FFFFF
        val bSig  = (BigInt(1) << 23) | bFrac

        assert(aSign == 0)
        assert(aExp  == 127)
        assert(aFrac == 0x400000)
        assert(aSig  == 0xC00000L)

        assert(bSign == 0)
        assert(bExp  == 128)
        assert(bFrac == 0x100000)
        assert(bSig  == 0x900000L)

        println("Result : PASS")
      }
  }
}



import chisel3._
import chiseltest._
import org.scalatest.flatspec.AnyFlatSpec

class FP32AdderTest extends AnyFlatSpec with ChiselScalatestTester {

  behavior of "FP32Adder"

  /*
   * 将 Scala Float 的 IEEE-754 单精度编码
   * 转换成 32 位无符号整数，作为硬件输入。
   */
  def floatBits(x: Float): BigInt = {
    BigInt(
      java.lang.Float.floatToRawIntBits(x) & 0xffffffffL
    )
  }

  /*
   * 将 32 位 IEEE-754 编码转换为十六进制字符串，
   * 便于观察仿真结果。
   */
  def hex32(x: BigInt): String = {
    f"0x${x.longValue}%08X"
  }

  /*
   * 单组测试函数
   */
  def check(
      c: FP32Adder,
      a: Float,
      b: Float,
      expected: Float,
      name: String
  ): Unit = {

    val aBits        = floatBits(a)
    val bBits        = floatBits(b)
    val expectedBits = floatBits(expected)

    c.io.a.poke(aBits.U)
    c.io.b.poke(bBits.U)

    // 本实验模块为组合逻辑。
    // step 一拍主要用于使测试波形更加清晰。
    c.clock.step()

    val actualBits = c.io.y.peek().litValue

    println("----------------------------------------")
    println(s"Test : $name")
    println(s"A        = $a")
    println(s"B        = $b")
    println(s"Expected = $expected")
    println(s"A bits        = ${hex32(aBits)}")
    println(s"B bits        = ${hex32(bBits)}")
    println(s"Expected bits = ${hex32(expectedBits)}")
    println(s"Actual bits   = ${hex32(actualBits)}")

    // 自动判断结果
    c.io.y.expect(expectedBits.U)

    println("Result : PASS")
  }


  it should "pass all required FP32 addition tests" in {

    /*
     * 生成 VCD 波形。
     * 学生可以使用 GTKWave 观察内部数据变化。
     */
    test(new FP32Adder)
      .withAnnotations(Seq(WriteVcdAnnotation)) { c =>

        // =====================================================
        // 1. 基本正数加法
        // =====================================================

        check(
          c,
          1.0f,
          2.0f,
          3.0f,
          "Basic addition"
        )

        // =====================================================
        // 2. 同号、具有小数部分
        // =====================================================

        check(
          c,
          1.5f,
          2.25f,
          3.75f,
          "Fraction addition"
        )

        // =====================================================
        // 3. 异号加法
        // =====================================================

        check(
          c,
          5.5f,
          -2.25f,
          3.25f,
          "Different signs"
        )

        // =====================================================
        // 4. 完全抵消
        // =====================================================

        check(
          c,
          1.0f,
          -1.0f,
          0.0f,
          "Cancellation"
        )

        // =====================================================
        // 5. 两个负数
        // =====================================================

        check(
          c,
          -3.0f,
          -4.0f,
          -7.0f,
          "Negative addition"
        )

        // =====================================================
        // 6. 阶码不同：
        //    可以重点观察 expDiff 和 smallAligned
        // =====================================================

        check(
          c,
          100.0f,
          0.125f,
          100.125f,
          "Exponent alignment"
        )


        // =====================================================
        // 以下两组专门用于实验过程观察
        // =====================================================

        // -----------------------------------------------------
        // 7. 对阶观察
        //
        // 1.0   = 1.0 × 2^0
        // 0.125 = 1.0 × 2^-3
        //
        // 阶差应为 3
        // 小数尾数需要右移 3 位
        // -----------------------------------------------------

        check(
          c,
          1.0f,
          0.125f,
          1.125f,
          "Alignment observation"
        )

        // -----------------------------------------------------
        // 8. 左规格化观察
        //
        // 1.0 + (-0.875)
        // = 0.125
        //
        // 尾数相减以后会出现多个前导 0，
        // 需要左移并减小阶码。
        // -----------------------------------------------------

        check(
          c,
          1.0f,
          -0.875f,
          0.125f,
          "Left normalization observation"
        )

      }
  }
}
