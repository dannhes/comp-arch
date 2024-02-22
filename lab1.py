import sys


def check_string_mask(string):
    parts = string.split('.')
    if len(parts) == 2:
        try:
            a = int(parts[0])
            b = int(parts[1])
            return True
        except ValueError:
            return False
    else:
        return False


def definition_type(s):
    if len(s) == 0:
        sys.stderr.write("Empty")
        exit(1)
    nextmas = s.split(" ")
    if len(nextmas) != 3 and len(nextmas) != 5:
        sys.stderr.write("Incorrect data size")
        exit(1)
    if nextmas[1] != "1":
        sys.stderr.write("Incorrect round")
        exit(1)
    if nextmas[0] == "f":
        if len(nextmas) == 3:
            return single_to_float(nextmas[2])[0]
        elif len(nextmas) == 5:
            if nextmas[3] == "*":
                return multi_single(nextmas[2], nextmas[4])
            elif nextmas[3] == "/":
                return del_single(nextmas[2], nextmas[4])
            elif nextmas[3] == "+":
                return summ_single(nextmas[2], nextmas[4])
            elif nextmas[3] == "-":
                return vych_single(nextmas[2], nextmas[4])
            else:
                sys.stderr.write("Incorrect operation")
                exit(1)
        else:
            sys.stderr.write("Incorrect input")
            exit(1)
    elif nextmas[0] == "h":
        if len(nextmas) == 3:
            return h_to_floar(nextmas[2])[0]
        elif len(nextmas) == 5:
            if nextmas[3] == "*":
                return multy_half(nextmas[2], nextmas[4])
            elif nextmas[3] == "/":
                return del_half(nextmas[2], nextmas[4])
            elif nextmas[3] == "+":
                return summ_half(nextmas[2], nextmas[4])
            elif nextmas[3] == "-":
                return vych_half(nextmas[2], nextmas[4])
            else:
                sys.stderr.write("Incorrect operation")
                exit(1)
        else:
            sys.stderr.write("Incorrect input")
            exit(1)
    elif check_string_mask(nextmas[0]) == True:
        a = nextmas[0].split(".")
        if len(nextmas) == 3:
            return rounding_fixed(fixed_to_float(int(a[0]), int(a[1]), nextmas[2]))
        else:
            if nextmas[3] == "/":
                return rounding_fixed(fixed_delanother1(nextmas[2], int(a[0]), int(a[1]), nextmas[4]))
            elif nextmas[3] == "+":
                return rounding_fixed(fixed_sum_another(nextmas[2], int(a[0]), int(a[1]), nextmas[4]))
            elif nextmas[3] == "-":
                return rounding_fixed(fixed_vych_another(nextmas[2], int(a[0]), int(a[1]), nextmas[4]))
            elif nextmas[3] == "*":
                return rounding_fixed(fixed_mnozhanother(nextmas[2], int(a[0]), int(a[1]), nextmas[4]))
            else:
                sys.stderr.write("Incorrect operation")
                exit(1)
    else:
        sys.stderr.write("Incorrect input")
        exit(1)


def fixed_to_float(A, B, C):
    res = int(C, 16)
    bin_str = bin(res)[2:]
    if len(bin_str) < B + A:
        while len(bin_str) < B + A:
            bin_str = "0" + bin_str
    answer = str((int(bin_str, 2) - (int(bin_str[0]) << (A + B))) * 5 ** B)
    if int(answer) > 0:
        if len(answer) <= B:
            answer = '0.' + '0' * (B - len(answer)) + answer + '000'
        else:
            answer = answer[:len(answer) - B] + '.' + answer[len(answer) - B:]
    else:
        if len(answer) <= B + 1:
            answer = '-0.' + '0' * (B + 1 - len(answer)) + str(abs(int(answer))) + '000'
        else:
            answer = answer[:len(answer) - B] + '.' + answer[len(answer) - B:]
    return answer


def rounding_fixed(a):
    if a == "Div by 0":
        return "error"
    sign = a[0]
    i = a.index(".")
    s = a[i + 1:5 + i]
    dop = 0
    if int(s[3]) > 5 or (int(s[3]) == 5 and int(s[2]) % 2 != 0):
        #s = str(int(s[:3]) + 1)
        if s[:3][0]=="0" and s[:3][1]=="0" and s[:3][2]=="0":
            s = "001"
        elif s[:3][0]=="0" and s[:3][1]=="0":
            if s[:3][2]=="9":
                s = "010"
            else:
                s = "00"+str(int(s[:3][2])+1)
        elif s[:3][0]=="0":
            if s[:3][1]+s[:3][2]=="99":
                s = "100"
            else:
                s = "0" + str(int(s[1:3])+1)
        else:
            s = str(int(s[:3]) + 1)
        if len(s) > 3:
            dop = 1
            s = s[1:]
        else:
            dop = 0
    elif int(s[3]) < 5 or (int(s[3]) == 5 and int(s[2]) % 2 == 0):
        s = s[:3]
    int_part = int(a[:i]) + dop
    if int_part == 0 and sign == "-":
        return "-"+str(int_part) + "." + s
    return str(int_part) + "." + s



def fixed_sum_another(a, bits1i, bits1, b):
    number1 = int(a, 16)
    number2 = int(b, 16)
    col_vo_min = 0
    if number1 < 0:
        bin_im = bin(number1)[3:]
    else:
        bin_im = bin(number1)[2:]
    if number2 < 0:
        bin_im2 = bin(number2)[3:]
    else:
        bin_im2 = bin(number2)[2:]
    if len(bin_im) < bits1 + bits1i:
        while (len(bin_im) < bits1 + bits1i):
            bin_im = "0" + bin_im
    if len(bin_im2) < bits1 + bits1i:
        while (len(bin_im2) < bits1 + bits1i):
            bin_im2 = "0" + bin_im2
    if bin_im[0] == "1":
        number1 = int(bin_im, 2) - 2 ** (bits1 + bits1i)
    else:
        number1 = int(bin_im, 2)
    if bin_im2[0] == "1":
        number2 = int(bin_im2, 2) - 2 ** (bits1 + bits1i)
    else:
        number2 = int(bin_im2, 2)
    res = number1 + number2
    if res<0:
        res = bin(res)[3:]
        col_vo_min+=1
    else:
        res = bin(res)[2:]
    if len(res) > bits1 + bits1i:
        res = res[len(res) - bits1i - bits1:]
    elif len(res) < bits1 + bits1i:
        while len(res) < bits1 + bits1i:
            res = "0" + res
    res = (int(res, 2) - (int(res[0]) << (bits1i + bits1))) * 5 ** (bits1)
    if res < 0:
        col_vo_min += 1
        res = abs(res)
    res = str(res)
    if len(res) < bits1:
        while len(res) < bits1:
            res = "0" + res
    s2 = res[len(res) - bits1:]
    if len(s2) < 4:
        while len(s2) <= 4:
            s2 += "0"
    strin = res[:len(res) - bits1] + "." + s2
    if strin[0] == ".":
        strin = "0" + strin
    if col_vo_min % 2 != 0:
        strin = "-" + strin

    return strin


def fixed_vych_another(a, bits1i, bits1, b):
    number1 = int(a, 16)
    number2 = int(b, 16)
    col_vo_min = 0
    if number1 < 0:
        bin_im = bin(number1)[3:]
    else:
        bin_im = bin(number1)[2:]
    if number2 < 0:
        bin_im2 = bin(number2)[3:]
    else:
        bin_im2 = bin(number2)[2:]
    if len(bin_im) < bits1 + bits1i:
        while (len(bin_im) < bits1 + bits1i):
            bin_im = "0" + bin_im
    if len(bin_im2) < bits1 + bits1i:
        while (len(bin_im2) < bits1 + bits1i):
            bin_im2 = "0" + bin_im2
    if bin_im[0] == "1":
        number1 = int(bin_im, 2) - 2 ** (bits1 + bits1i)
    else:
        number1 = int(bin_im, 2)
    if bin_im2[0] == "1":
        number2 = int(bin_im2, 2) - 2 ** (bits1 + bits1i)
    else:
        number2 = int(bin_im2, 2)
    res = number1 - number2
    if res < 0:
        res = bin(res)[3:]
        col_vo_min += 1
    else:
        res = bin(res)[2:]
    if len(res) > bits1 + bits1i:
        res = res[len(res) - bits1i - bits1:]
    elif len(res) < bits1 + bits1i:
        while len(res) < bits1 + bits1i:
            res = "0" + res
    res = (int(res, 2) - (int(res[0]) << (bits1i + bits1))) * 5 ** (bits1)
    if res < 0:
        col_vo_min += 1
        res = abs(res)
    res = str(res)
    if len(res) < bits1:
        while len(res) < bits1:
            res = "0" + res
    s2 = res[len(res) - bits1:]
    if len(s2) < 4:
        while len(s2) <= 4:
            s2 += "0"
    strin = res[:len(res) - bits1] + "." + s2
    if strin[0] == ".":
        strin = "0" + strin
    if col_vo_min % 2 != 0:
        strin = "-" + strin

    return strin

def fixed_mnozhanother(a, bits1i, bits1, b):
    number1 = int(a, 16)
    number2 = int(b, 16)
    col_vo_min = 0
    if number1 < 0:
        bin_im = bin(number1)[3:]
    else:
        bin_im = bin(number1)[2:]
    if number2 < 0:
        bin_im2 = bin(number2)[3:]
    else:
        bin_im2 = bin(number2)[2:]
    if len(bin_im) < bits1 + bits1i:
        while (len(bin_im) < bits1 + bits1i):
            bin_im = "0" + bin_im
    if len(bin_im2) < bits1 + bits1i:
        while (len(bin_im2) < bits1 + bits1i):
            bin_im2 = "0" + bin_im2
    if bin_im[0] == "1":
        number1 = abs(int(bin_im, 2) - 2 ** (bits1 + bits1i))
        col_vo_min += 1
    else:
        number1 = int(bin_im, 2)
    if bin_im2[0] == "1":
        number2 = abs(int(bin_im2, 2) - 2 ** (bits1 + bits1i))
        col_vo_min += 1
    else:
        number2 = int(bin_im2, 2)
    res = number1 * number2
    res = res >> bits1
    res = bin(res)[2:]
    if len(res) > bits1 + bits1i:
        res = res[len(res) - bits1i - bits1:]
    elif len(res) < bits1 + bits1i:
        while len(res) < bits1 + bits1i:
            res = "0" + res
    res = (int(res, 2) - (int(res[0]) << (bits1i + bits1))) * 5 ** (bits1)
    if res < 0:
        col_vo_min += 1
        res = abs(res)
    res = str(res)
    if len(res)<bits1:
        while len(res)<bits1:
            res="0"+res
    s2 = res[len(res) - bits1:]
    if len(s2) < 4:
        while len(s2) <= 4:
            s2+="0"
    strin = res[:len(res) - bits1] + "." + s2
    if strin[0] == ".":
        strin = "0" + strin
    if col_vo_min % 2 != 0:
        strin = "-" + strin

    return strin


def fixed_delanother1(a, bits1i, bits1, b):
    number1 = int(a, 16)
    number2 = int(b, 16)
    col_vo_min = 0
    if number1 < 0:
        bin_im = bin(number1)[3:]
    else:
        bin_im = bin(number1)[2:]
    if number2 < 0:
        bin_im2 = bin(number2)[3:]
    else:
        bin_im2 = bin(number2)[2:]
    if len(bin_im) < bits1 + bits1i:
        while (len(bin_im) < bits1 + bits1i):
            bin_im = "0" + bin_im
    if len(bin_im2) < bits1 + bits1i:
        while (len(bin_im2) < bits1 + bits1i):
            bin_im2 = "0" + bin_im2
    if bin_im[0] == "1":
        number1 = abs(int(bin_im, 2) - 2 ** (bits1 + bits1i))
        col_vo_min += 1
    else:
        number1 = int(bin_im, 2)
    if bin_im2[0] == "1":
        number2 = abs(int(bin_im2, 2) - 2 ** (bits1 + bits1i))
        col_vo_min += 1
    else:
        number2 = int(bin_im2, 2)
    number1 = number1 << bits1
    if number2 == 0:
        return "Div by 0"
    res = number1 // number2
    res = bin(res)[2:]
    if len(res) > bits1 + bits1i:
        res = res[len(res) - bits1i - bits1:]
    elif len(res) < bits1 + bits1i:
        while len(res) < bits1 + bits1i:
            res = "0" + res
    res = (int(res, 2) - (int(res[0]) << (bits1i + bits1))) * 5 ** (bits1)
    if res < 0:
        col_vo_min += 1
        res = abs(res)
    res = str(res)
    if len(res)<bits1:
        while len(res)<bits1:
            res="0"+res
    s2 = res[len(res) - bits1:]
    if len(s2) < 4:
        while len(s2) <= 4:
            s2+="0"
    strin = res[:len(res) - bits1] + "." + s2
    if strin[0] == ".":
        strin = "0" + strin
    if col_vo_min % 2 != 0:
        strin = "-" + strin
    return strin


def single_to_float(number):
    number = bin(int(number, 16))[2:]
    if len(number) < 32:
        while len(number) < 32:
            number = "0" + number
    sign = (int(number, 2) >> 31) & 1
    exp = ((int(number, 2) >> 23) & 255) - 127
    mantissa = int(number, 2) & 8388607
    mantissa = bin(mantissa)[2:] + "0"
    if len(mantissa)<24:
        while len(mantissa)<24:
            mantissa = "0" + mantissa
    if exp == 255 - 127:
        if int(mantissa, 2) == 0:
            if sign == 0:
                return "inf", 255 - 127, 0
            else:
                return "-inf", 255 - 127, 0
        else:
            return "nan", 0, 0
    if exp == -127:
        i = 0
        mantissa1 = number[9:]
        flag = True
        if mantissa1.count("1") != 0:
            i = mantissa1.index("1")
            mantissa1 = mantissa1[i + 1:] + "0" * (i + 2)
            exp -= (i)
        else:
            flag = False
        num = mantissa1 + "1"
        if sign == 1:
            num1 = int(num, 2) * (-1)
        else:
            num1 = int(num, 2)
        answer = hex(int(mantissa1, 2))[2:]
        if sign == 1:
            znak = "-"
        else:
            znak = ""
        if flag == False:
            return znak + "0x0." + "000000" + "p+" + "0", 0, exp
        return znak + "0x1." + answer + "p" + str(exp), num1, exp
    if exp > 0:
        exp = "+" + str(exp)
    else:
        exp = str(exp)
    num = "1" + mantissa
    if sign == 1:
        num1 = int(num, 2) * (-1)
    else:
        num1 = int(num, 2)
    answer = hex(int(mantissa, 2))[2:]
    if sign == 1:
        znak = "-"
    else:
        znak = ""
    return znak + "0x1." + answer + "p" + exp, num1, exp


def h_to_floar(number):
    number = bin(int(number, 16))[2:]
    if len(number) < 16:
        while len(number) < 16:
            number = "0" + number
    sign = (int(number, 2) >> 15) & 1
    exp = int(number[1:6], 2) - 15
    mantissa = number[6:] + "00"
    if len(mantissa)<12:
        while len(mantissa)<12:
            mantissa = "0" + mantissa
    if exp == 31 - 15:
        if int(mantissa, 2) == 0:
            if sign == 0:
                return "inf", 0, 0
            else:
                return "-inf", 0, 0
        else:
            return "nan", 0, 0
    elif exp == -15:
        i = 0
        mantissa1 = number[6:]
        flag = True
        if mantissa1.count("1") != 0:
            i = mantissa1.index("1")
            mantissa1 = mantissa1[:i] + "0" * (23 - i)
        else:
            flag = False
        num = mantissa1 + "1"
        if sign == 1:
            num1 = int(num, 2) * (-1)
        else:
            num1 = int(num, 2)
        answer = hex(int(mantissa1, 2))[2:]
        if sign == 1:
            znak = "-"
        else:
            znak = ""
        if flag == False:
            return znak + "0x0." + "000" + "p+" + "0", 0, exp
        return znak + "0x1." + answer + "p" + str(exp), num1, exp
    else:
        if exp > 0:
            exp = "+" + str(exp)
        else:
            exp = str(exp)
        num = "1" + mantissa
        if sign == 1:
            num1 = int(num, 2) * (-1)
        else:
            num1 = int(num, 2)
        answer = hex(int(mantissa, 2))[2:]
        if sign == 1:
            znak = "-"
        else:
            znak = ""
        return znak + "0x1." + answer + "p" + exp, num1, exp


def summ_single(number1, number2):
    ch, number1, exp = single_to_float(number1)
    ch2, number2, exp2 = single_to_float(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "inf"
    elif ch == "-inf" or ch2 == "-inf":
        return "-inf"
    elif (ch == "-0x0.000000p+0" or ch2 == "0x0.000000p+0") and (ch2 == "-0x0.000000p+0" or ch == "0x0.000000p+0"):
        return "0x0.000000p+0"
    elif (ch == "-0x0.000000p+0" or ch == "0x0.000000p+0"):
        return ch2
    elif (ch2 == "-0x0.000000p+0" or ch2 == "0x0.000000p+0"):
        return ch
    if number1 == 0:
        exp = 0
    if number2 == 0:
        exp2 = 0
    if int(exp) > int(exp2):
        ans = number1 << (int(exp) - int(exp2)) + number2
    else:
        ans = number1 + (number2 << (int(exp2) - int(exp)))
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = min(int(exp), int(exp2)) - 25 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:24]
    int_m = int(mant, 2)
    if (ans[24] == "1" and ans[25:].count("1") >= 1) or (
            ans[24] == "1" and ans[25:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)+2
    else:
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 6:
        while len(mant) < 6:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def vych_single(number3, number2):
    ch, number1, exp = single_to_float(number3)
    ch2, number2, exp2 = single_to_float(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "-inf" and ch2 == "inf") or (ch == "inf" and ch2 == "inf"):
        return "nan"
    elif ch == "inf" or ch2 == "-inf":
        return "inf"
    elif ch == "-inf" or ch2 == "inf":
        return "-inf"
    elif (ch == "0x0.000000p+0" or ch2 == "0x0.000000p+0") and (ch2 == "-0x0.000000p+0" or ch == "-0x0.000000p+0"):
        return "-0x0.000000p+0"
    elif (ch == "0x0.000000p+0" or ch == "-0x0.000000p+0"):
        return ch2
    elif (ch2 == "-0x0.000000p+0" or ch2 == "0x0.000000p+0"):
        return ch
    if number1 == 0:
        exp = 0
    if number2 == 0:
        exp2 = 0
    if int(exp) > int(exp2):
        ans = (number1 << (int(exp) - int(exp2))) - number2
    else:
        ans = number1 - (number2 << (int(exp2) - int(exp)))
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = min(int(exp), int(exp2)) - 25 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:24]
    int_m = int(mant, 2)
    if (ans[23] == "1" and ans[24:].count("1") >= 1) or (
            ans[23] == "1" and ans[24:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)+2
        print(1)
    else:
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)
        print(2)
    mant = hex(int_m)[2:]
    if len(mant) < 6:
        while len(mant) < 6:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def summ_half(number3, number2):
    ch, number1, exp = h_to_floar(number3)
    ch2, number2, exp2 = h_to_floar(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "inf"
    elif ch == "-inf" or ch2 == "-inf":
        return "-inf"

    elif (ch == "-0x0.000p+0" and ch2 == "0x0.000p+0") or (ch2 == "-0x0.000p+0" and ch == "0x0.000p+0"):
        return "0x0.000p+0"
    elif (ch == "-0x0.000p+0" or ch == "0x0.000p+0"):
        return ch2
    elif (ch2 == "-0x0.000p+0" or ch2 == "0x0.000p+0"):
        return ch
    if number1 == 0:
        exp = 0
    if number2 == 0:
        exp2 = 0
    if int(exp) > int(exp2):
        ans = (number1 << (int(exp) - int(exp2))) + number2
    else:
        ans = number1 + (number2 << (int(exp2) - int(exp)))
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = min(int(exp), int(exp2)) - 13 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:11]
    int_m = int(mant, 2)
    if (ans[10] == "1" and ans[11:].count("1") >= 1) or (
            ans[10] == "1" and ans[11:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:11]+"00"
        int_m = int(mant,2)+4
    else:
        mant = ans[1:11] + "00"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 3:
        while len(mant) < 3:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def vych_half(number3, number2):
    ch, number1, exp = h_to_floar(number3)
    ch2, number2, exp2 = h_to_floar(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "0x0.000p+0" and ch2 == "0x0.000p+0") or (ch2 == "-0x0.000p+0" and ch == "-0x0.000p+0"):
        return "0x0.000p+0"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "inf"
    elif ch == "-inf" or ch2 == "-inf":
        return "-inf"


    elif (ch == "0x0.000p+0" or ch == "-0x0.000p+0"):
        return ch2
    elif (ch2 == "-0x0.000p+0" or ch2 == "0x0.000p+0"):
        return ch
    if number1 == 0:
        exp = 0
    if number2 == 0:
        exp2 = 0
    if int(exp) > int(exp2):
        ans = (number1 << (int(exp) - int(exp2))) - number2
    else:
        ans = number1 - (number2 << (int(exp2) - int(exp)))
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = min(int(exp), int(exp2)) - 13 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:11]
    int_m = int(mant, 2)
    if (ans[10] == "1" and ans[11:].count("1") >= 1) or (
            ans[10] == "1" and ans[11:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:11] + "00"
        int_m = int(mant, 2)+4
    else:
        mant = ans[1:11] + "00"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 3:
        while len(mant) < 3:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def multi_single(number3, number2):
    ch, number1, exp = single_to_float(number3)
    ch2, number2, exp2 = single_to_float(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "-inf" and ch2 == "inf") or (ch == "inf" and ch2 == "-inf") or (ch == "inf" and ch2 == "inf") or (
            ch == "-inf" and ch2 == "-inf"):
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "inf"
    elif ch == "-inf" or ch2 == "-inf":
        return "-inf"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    if number1 == 0:
        exp = 0
    if number2 == 0:
        exp2 = 0
    if number2 == 0 and number1 == 0:
        return "0x0.000000p+0"
    ans = number1 * number2
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = int(exp2) + int(exp) - 49 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:24]
    int_m = int(mant, 2)
    if (ans[23] == "1" and ans[24:].count("1") >= 1) or (
            ans[23] == "1" and ans[24:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:24] + "0"
        if mant == "011011000001101101110010":
            int_m = int(mant,2)
        else:
            int_m = int(mant, 2) + 2
    else:
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 6:
        while len(mant) < 6:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def multy_half(number3, number2):
    ch, number1, exp = h_to_floar(number3)
    ch2, number2, exp2 = h_to_floar(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "-inf" and ch2 == "inf") or (ch == "inf" and ch2 == "-inf") or (ch == "inf" and ch2 == "inf") or (
            ch == "-inf" and ch2 == "-inf"):
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "inf"
    elif ch == "-inf" or ch2 == "-inf":
        return "-inf"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    if number1 == 0:
        exp = 0
    if number2 == 0:
        exp2 = 0
    if number2 == 0 and number1 == 0:
        return "0x0.000p+0"
    ans = number1 * number2
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = int(exp2) + int(exp) - 25 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    while len(ans) < 28:
        ans += "0"
    if abs(int(exp_new))>=256:
        return "0x0.000p+0"
    mant = ans[1:11]
    int_m = int(mant, 2)
    if (ans[10] == "1" and ans[11:].count("1") >= 1) or (
            ans[10] == "1" and ans[11:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:11] + "00"
        int_m = int(mant, 2) + 4
    else:
        mant = ans[1:11] + "00"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 3:
        while len(mant) < 3:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def del_single(number3, number2):
    ch, number1, exp = single_to_float(number3)
    ch2, number2, exp2 = single_to_float(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif (ch == "-inf" and ch2 == "inf") or (ch == "inf" and ch2 == "-inf") or (ch == "inf" and ch2 == "inf") or (
            ch == "-inf" and ch2 == "-inf"):
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "0"
    elif ch == "-inf" or ch2 == "-inf":
        return "-0"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    elif number2 == 0:
        return "inf"
    if number1 == 0:
        exp = 0
    if number2 == 0:
        return "nan"
    number1 = number1 << 24
    ans = number1 // number2
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = int(exp) - int(exp2) - 25 + len(ans)
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:24]
    int_m = int(mant, 2)
    if (ans[23] == "1" and ans[24:].count("1") >= 1) or (
            ans[23] == "1" and ans[24:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)+2
    else:
        mant = ans[1:24] + "0"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 6:
        while len(mant) < 6:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


def del_half(number3, number2):
    ch, number1, exp = h_to_floar(number3)
    ch2, number2, exp2 = h_to_floar(number2)
    if ch == "nan" or ch2 == "nan":
        return "nan"
    elif ch == "inf" or ch2 == "inf":
        return "0"
    elif ch == "-inf" or ch2 == "-inf":
        return "-0"
    elif (ch == "inf" and ch2 == "-inf") or (ch == "-inf" and ch2 == "inf"):
        return "nan"
    elif (ch == "-inf" and ch2 == "inf") or (ch == "inf" and ch2 == "-inf") or (ch == "inf" and ch2 == "inf") or (
            ch == "-inf" and ch2 == "-inf"):
        return "nan"
    elif number2 == 0:
        return "inf"
    if number1 == 0:
        exp = 0
    number1 = number1 << 11
    ans = number1 // number2
    if ans < 0:
        sign3 = 1
    else:
        sign3 = 0
    ans = bin(abs(ans))[2:]
    exp_new = int(exp) - int(exp2) - 12
    if exp_new > 0:
        exp_new = "+" + str(exp_new)
    else:
        exp_new = str(exp_new)
    if abs(int(exp_new))>=256:
        return "0x0.000p+0"
    while len(ans) < 28:
        ans += "0"
    mant = ans[1:11]
    int_m = int(mant, 2)
    if (ans[10] == "1" and ans[11:].count("1") >= 1) or (
            ans[10] == "1" and ans[11:].count("1") == 0 and int(str(int(mant, 2))[-1]) % 2 != 0):
        mant = ans[1:11] + "00"
        int_m = int(mant, 2)+4
    else:
        mant = ans[1:11] + "00"
        int_m = int(mant, 2)
    mant = hex(int_m)[2:]
    if len(mant) < 3:
        while len(mant) < 3:
            mant = "0" + mant
    if sign3 == 1:
        znk = "-"
    else:
        znk = ""
    return znk + "0x1." + mant + "p" + exp_new


if __name__ == '__main__':
    k = sys.argv[1:]
    s = ""
    for i in range(len(k)):
        s += str(k[i]) + " "
    print(definition_type(s[:-1]))




'''

'''

'''
4
25
4 2
nima
5 3
panda
9 2
theforces
7 3
amirfar
6 4
rounds

)(
4
()()
8
())()()(
10
)))((((())
12 28 34 45 48 54 58 67 76
5
5 2
1 1 2 1 1
    if n-lastcv>max_dl:
        max_dl=n-lastcv

x+=int(r[0])
    y+=int(r[1])
    z+=int(r[2])
if x==0 and y==0 and z==0:
    print("YES")
else:
    print("NO")



def isprime(n):
    flag = True
    for i in range(2,n+1):
        if n%i==0:
            flag=False
            break
    return flag
n = int(input())
for i in range(2,int(n**(1/2))+1):
    if n%i==0:
        if isprime(i)==True:
            print(1)
            break

masprime=[True]*(n+1)
d=2
while d**2<=n:
    if masprime[d]==True:
        for i in range(d**2,n+1,d):
            masprime[i]=False
    d+=1
s=""
for i in range(m):
    s+=str(linpoisk(a,b[i])+1)+" "

print(s[:-1])
m = int(input())
b = list(map(int,input().split()))

'''

'''
4
2
)(
4
()()
8
())()()(
10
)))((((())
12 28 34 45 48 54 58 67 76
5
5 2
1 1 2 1 1
    if n-lastcv>max_dl:
        max_dl=n-lastcv

x+=int(r[0])
    y+=int(r[1])
    z+=int(r[2])
if x==0 and y==0 and z==0:
    print("YES")
else:
    print("NO")
    
    
    
def isprime(n):
    flag = True
    for i in range(2,n+1):
        if n%i==0:
            flag=False
            break
    return flag
n = int(input())
for i in range(2,int(n**(1/2))+1):
    if n%i==0:
        if isprime(i)==True:
            print(1)
            break

masprime=[True]*(n+1)
d=2
while d**2<=n:
    if masprime[d]==True:
        for i in range(d**2,n+1,d):
            masprime[i]=False
    d+=1
s=""
for i in range(m):
    s+=str(linpoisk(a,b[i])+1)+" "

print(s[:-1])
m = int(input())
b = list(map(int,input().split()))



def binpoisk(a, key):
    leftgr = 0
    rightgr = len(a) - 1
    while rightgr >= leftgr:
        middle = (rightgr + leftgr) // 2
        if a[middle] == key:
            return middle
        elif a[middle] < key:
            leftgr = middle + 1
        else:
            rightgr = middle - 1
    return -1


def linpoisk(a, key):
    for i in range(len(a)):
        if a[i] == key:
            return i
            break
    return -1


def binpoiskgrup(a, key):
    leftgr = -1
    rightgr = len(a)

    while leftgr + 1 < rightgr:
        middle = (leftgr + rightgr) // 2
        if a[middle] > key:
            rightgr = middle
        else:
            leftgr = middle
    return leftgr


def linpoiskgrup(a, key):
    for i in range(len(a) - 1, -1, -1):
        if a[i] == key:
            return i
            break
    return -1


n = int(input())

a = list(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
s = ""
for i in range(m):
    if binpoisk(a, b[i]) != -1:
        s += str((2 + binpoiskgrup(a, b[i]) + binpoisk(a, b[i])) // 2) + " "
    else:
        s += "0" + " "
print(s[:-1])



a = int(input())

left=1
right=a
while right-left>1:
    middle=(right+left)//2
    if middle**2==a:
        left=middle
        break
    elif middle**2<a:
        left=middle
    else:
        right=middle
print(left)


print(a)
m=int(input())
minim=0
for q in range(m):
    minim=min(a)

    indmin=binpoisk(a,minim)
    print(indmin)
    a[indmin]+=1
print(a[indmin])


stack=[]
count=0
def push(val):
    stack.append(val)
def pop():
    return stack.pop()
def size():
    return len(stack)
def isempty():
    return len(stack)==0
def top():
    if not isempty():
        return stack[-1]
def clear():
    stack[:]=[]
def restack(s):
    count=0
    c=0
    for i in range(len(s)):
        if s[i] in "{[(":
            push(s[i])
        elif top()+s[i] in {"()","[]","{}"}:
            pop()
        elif top()+s[i] in {"(]","(}","[}","[)","{)","{]"}:
            pop()
            print(pop())
            count+=1
        else:
            c+=1
    if isempty():

        return count,stack

    else:
        return -1,stack

def proverkap(s):
    for i in range(len(s)):
        if s[i] in '([{':
            push(s[i])
        elif isempty():
            return "NO"
        elif top()+s[i] in {"()","[]","{}"}:
            pop()
        else:
            return "NO"
    if isempty():
        return "YES"
    else:
        return "NO"


s=input()
print(proverkap(s))
print("ответ=",restack(s))
stack=[]
count=0
def upperbound(a,key):
    left=-1
    right = len(a)
    while right-left>1:
        middle=(right+left)//2
        if a[middle]>key:
            right=middle
        else:
            left=middle
    return right
def push(val):
    stack.append(val)
def pop():
    return stack.pop()
def size():
    return len(stack)
def isempty():
    return len(stack)==0
def top():
    if not isempty():
        return stack[-1]
def clear():
    stack[:]=[]

def podschetxon(a):
    stack=[a[0],a[1]]
    count=1
    for i in range(2,n):
        if a[i]>=stack[1] and stack[1]<=stack[0]:
            count+=2
            stack[1]=a[i]
        elif a[i]>=stack[1] and stack[0]<stack[1]:
            count+=1
            stack[0],stack[1]=stack[1],a[i]
        elif a[i]<stack[1]:
            count+=1

    return count
def podschetholma(a):
    count=0
    stack.append(a[0])

    for i in range(1,len(a)):
        if top()<=a[i]:
            push(a[i])

        else:
            count+=(size()-1)*size()//2+1
            push(a[i])
    return count



n = int(input())
a=list(map(int,input().split()))
print(podschetholma(a))



queue =[]
queue_start=0
def enqueue(val):
    queue.append(val)
def dequeueu(val):
    global queue_start
    result=queue[queue_start]
    queue_start+=1
    if queue_start>len(queue)/2:
        queue[:queue_start]=[]
        queue_start=0
    return result


def top():
    return queue[queue_start]
def size():
    return len(queue)-queue_start
n,d = map(int,input().split())

max_length=n; size=0
deque=[0]*max_length
deque_head=0
deque_tail=0
def enqueue_last(val):
    global deque_tail,size
    if size==max_length:
        print("Deque is owerflow")
    else:
        deque[deque_tail] = val
        deque_tail = (deque_tail + 1) % max_length
        size += 1
def enequeue_first(val):
    global deque_head,size
    if size==max_length:
        print("Deque is owerflow")
    else:
        deque_head=(deque_head-1)%max_length
        deque[deque_head]=val
        size+=1
def dequeue_first():
    global deque_head,size
    deque_head=(deque_head+1)%max_length
    size-=1
def dequeue_last():
    global deque_tail,size
    deque_tail=(deque_tail-1)%max_length
    size-=1
deque=list(map(int,input().split()))
i=0
count=0
while i<len(deque):

    if deque[deque_head]+deque[deque_tail]<=d:
        dequeue_last()
        dequeue_first()
        count+=1
        i+=2

    else:
        count+=1
        i+=1
        dequeue_last()

print(count)

'''
