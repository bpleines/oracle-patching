def splitUnderscore(string):
    oneoffDirectory, binaryOverview, osVersion = string.split("_")
    return oneoffDirectory

def splitSidString(string):
    sid_list = string.split(",")
    return sid_list
        
def opatchLog(string):
    opatchOutput = string
    beforeLogfilePath, includesLogfilePath = opatchOutput.split("Log file location :", 1)
    logfilePathExtraChars, afterLogfilePath = includesLogfilePath.split("Verifying", 1)
    return logfilePathExtraChars

def binary_specific_oracle_sid(string):
    lsnrGrepString = string
    dictionaryString = ' '.join(lsnrGrepString.split(" "))
    longString, oracleSidString = dictionaryString.split("tnslsnr ")
    oracleSid, inheritFlag = oracleSidString.split(" ")
    return oracleSid

def binary_specific_database_oracle_sid(string):
    oracleSidString = string
    sid, binaryhome = oracleSidString.split(" ")
    return sid

def splitVersion(string):
    versionString = string
    version, rest = string.split(".",1)
    return version

class FilterModule(object):
    def filters(self):
        return {
            'splitUnderscore': splitUnderscore,
            'splitSidString': splitSidString,
            'opatchLog' : opatchLog,
            'binary_specific_oracle_sid': binary_specific_oracle_sid,
            'binary_specific_database_oracle_sid': binary_specific_database_oracle_sid,
            'splitVersion': splitVersion
            }
