#!/usr/bin/env bash
# 把 ARM GCC 工具链加入 PATH。
# 用法:  source tools/toolchain_env.sh
#
# winget 安装的 GNU Arm Embedded Toolchain 不在 Claude Code 启动时继承的
# PATH 中, 因此每次编译前 source 一次本文件即可。

ARM_GCC_DIR="/c/Program Files (x86)/Arm GNU Toolchain arm-none-eabi/14.2 rel1/bin"

if [ -d "$ARM_GCC_DIR" ]; then
  case ":$PATH:" in
    *":$ARM_GCC_DIR:"*) ;;
    *) export PATH="$ARM_GCC_DIR:$PATH" ;;
  esac
  echo "ARM GCC: $(arm-none-eabi-gcc --version | head -1)"
else
  echo "警告: 未找到 $ARM_GCC_DIR" >&2
fi

# mingw32-make 作为 make 的别名 (Git for Windows 自带)
if ! command -v make >/dev/null 2>&1 && command -v mingw32-make >/dev/null 2>&1; then
  make() { mingw32-make "$@"; }
  export -f make
  echo "make -> mingw32-make"
fi
