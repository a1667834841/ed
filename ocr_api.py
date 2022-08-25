import ddddocr


def ocr_captcha(img:bytes):
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(img)
    # print(res)
    return res


