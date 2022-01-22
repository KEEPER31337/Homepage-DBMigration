
# Input xpress engine database extravars.
# Output student number as dictionary

# O:8:"stdClass":5:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:11:"birthday_ui";s:10:"1998-09-24";s:21:"__profile_image_exist";s:5:"false";s:12:"phone_number";a:3:{i:0;s:3:"010";i:1;s:4:"1234";i:2;s:4:"5678";}s:13:"studentnumber";s:9:"201724539";}
# O:8:"stdClass":2:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:21:"__profile_image_exist";s:5:"false";}
# O:8:"stdClass":4:{s:15:"xe_validator_id";s:20:"modules/member/tpl/1";s:11:"birthday_ui";s:10:"0000-00-00";s:21:"__profile_image_exist";s:5:"false";s:12:"phone_number";a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}}

def parseValue(rawValue) :
    return rawValue.split(':')[-1].strip('\"')

def parseStudentNumber(splitedExtraVars) :
    studentNumberKey = "s:13:\"studentnumber\""
    
    try :
        studentNumberKeyIndex = splitedExtraVars.index(studentNumberKey)
    except ValueError as ve :
        print(f"{ve} : Student number key not found in extra_vars.")
        return ""
    
    studentNumberIndex = studentNumberKeyIndex + 1
    studentNumber = parseValue(splitedExtraVars[studentNumberIndex])
    
    print(f"Student number : {studentNumber}")
    return studentNumber


def parseExtraVars(extraVars) :
    splitedExtraVars = extraVars.split(';')
    splitedExtraVars = [x.strip('}').strip('{') for x in splitedExtraVars]

    valueParsed = {
        "student_number":parseStudentNumber(splitedExtraVars)
    }
    return valueParsed

if __name__ == "__main__" :
    extraVars = input()
    parseExtraVars(extraVars)