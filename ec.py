# Running this script will return an exit code, which translates as such:
# 0 = executed successfully, no known error codes provided.
# 1 = executed successfully, information on known error codes shown.
# 2 = bad arguments
# 3 = internal error
# 4 = failed to start process or attach to process(es).
# 5 = license error
import os, sys;

sModulePath = os.path.dirname(__file__);
sys.path = [sModulePath] + [sPath for sPath in sys.path if sPath.lower() != sModulePath.lower()];
from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

from mWindowsSDK import \
  fs0GetExceptionDefineName, \
  fs0GetHResultDefineName, \
  fs0GetNTStatusDefineName, \
  fs0GetWin32ErrorCodeDefineName, \
  HRESULT, \
  WIN32_FROM_HRESULT;
from foConsoleLoader import foConsoleLoader;
oConsole = foConsoleLoader();

NORMAL        = 0x0F07;
INFO          = 0x0F0A;
HILITE        = 0x0F0F;
ERROR         = 0x0F0C;
oConsole.uDefaultColor = NORMAL;

if __name__ == "__main__":
  auErrorCodesShown = [];
  def fbShowInformationForErrorCode(uErrorCode):
    if uErrorCode in auErrorCodesShown: return False;
    auErrorCodesShown.append(uErrorCode);
    bInformationFound = False;
    for (sTypeName, fs0GetDefineName) in (
      ("Win32 error code", fs0GetWin32ErrorCodeDefineName),
      ("NT status", fs0GetNTStatusDefineName),
      ("HRESULT", fs0GetHResultDefineName),
      ("exception code", fs0GetExceptionDefineName),
    ):
      s0DefineName = fs0GetDefineName(uErrorCode);
      if s0DefineName:
        oConsole.fOutput(
          NORMAL, sTypeName, " ",
          HILITE, "%d" % uErrorCode, NORMAL, " / ", HILITE, "0x%X" % uErrorCode,
          NORMAL, " = ", INFO, s0DefineName,
          NORMAL, ".",
        );
        bInformationFound = True;
    try:
      uWin32ErrorCode = WIN32_FROM_HRESULT(HRESULT(uErrorCode));
    except:
      pass;
    else:
      s0DefineName = fs0GetWin32ErrorCodeDefineName(uWin32ErrorCode);
      if s0DefineName:
        oConsole.fOutput(
          NORMAL, "HRESULT ",
          HILITE, "%d" % uErrorCode, NORMAL, " / ", HILITE, "0x%X" % uErrorCode,
          NORMAL, " = Win32 error code ",
          HILITE, "%d" % uWin32ErrorCode, NORMAL, " / ", HILITE, "0x%X" % uWin32ErrorCode,
          NORMAL, " = ", INFO, s0DefineName,
          NORMAL, ".",
        );
      else:
        oConsole.fOutput(
          NORMAL, "Win32 error code as HRESULT ",
          HILITE, "%d" % uErrorCode, NORMAL, " / ", HILITE, "0x%X" % uErrorCode,
          NORMAL, " = Win32 error code ",
          HILITE, "%d" % uWin32ErrorCode, NORMAL, " / ", HILITE, "0x%X" % uWin32ErrorCode,
          NORMAL, " = UNKNOWN.",
        );
      bInformationFound = True;

    if not bInformationFound:
      oConsole.fOutput(
        NORMAL, "?? ",
        ERROR, "%d" % uErrorCode, NORMAL, " / ", ERROR, "0x%X" % uErrorCode,
        NORMAL, " = UNKNOWN.",
      );
    return bInformationFound;
  bInformationFound = False;
  for sArgument in sys.argv[1:]:
    if sArgument.startswith("0x"):
      uErrorCode = int(sArgument[2:], 16);
      if fbShowInformationForErrorCode(uErrorCode):
        bInformationFound = True;
    for uBase in (10, 16):
      try:
        uErrorCode = int(sArgument, uBase);
      except:
        pass;
      else:
        if fbShowInformationForErrorCode(uErrorCode):
          bInformationFound = True;
  sys.exit(0 if bInformationFound else 1);