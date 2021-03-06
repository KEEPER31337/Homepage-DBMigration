# Input xpress engine database extravars.
# Output student number as dictionary
from typing import Dict, List
from util.err import StringNotFoundErrorLog


class ExtraVarsParser:

    @classmethod
    def parseExtraVars(cls, extraVars: str) -> Dict[str, str]:
        splitedExtraVars = extraVars.split(';')
        splitedExtraVars = [x.strip('}').strip('{') for x in splitedExtraVars]

        studentNumber = cls.__parseStudentNumber(splitedExtraVars)
        studentNumber = studentNumber if cls.__checkStudentNumber(
            studentNumber) else None

        valueParsed = {"student_number": studentNumber}
        return valueParsed

    @classmethod
    def __parseStudentNumber(cls, splitedExtraVars: List[str]) -> str:
        studentNumberKey = "s:13:\"studentnumber\""

        try:
            studentNumberKeyIndex = splitedExtraVars.index(studentNumberKey)
        except ValueError as ve:
            print(StringNotFoundErrorLog(
                err=ve,
                className=cls.__name__,
                methodName=cls.__parseStudentNumber.__name__,
                stringFound=studentNumberKey,
                msg="Return empty string."))
            return ""

        studentNumberIndex = studentNumberKeyIndex + 1
        studentNumber = cls.__parseValue(splitedExtraVars[studentNumberIndex])

        return studentNumber

    @classmethod
    def __parseValue(cls, rawValue: str) -> str:
        return rawValue.split(':')[-1].strip('\"')

    @classmethod
    def __checkStudentNumber(cls, studentNumber: str) -> bool:
        if (not studentNumber) or len(studentNumber) == 2:
            return False
        return True

# Input example
# O:8:"stdClass":5:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:11:"birthday_ui";s:10:"1998-09-24";s:21:"__profile_image_exist";s:5:"false";s:12:"phone_number";a:3:{i:0;s:3:"010";i:1;s:4:"1234";i:2;s:4:"5678";}s:13:"studentnumber";s:9:"201724539";}
# O:8:"stdClass":2:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:21:"__profile_image_exist";s:5:"false";}
# O:8:"stdClass":4:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:11:"birthday_ui";s:10:"0000-00-00";s:21:"__profile_image_exist";s:5:"false";s:12:"phone_number";a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}}


if __name__ == "__main__":
    extraVars = input()
    ExtraVarsParser.parseExtraVars(extraVars)
