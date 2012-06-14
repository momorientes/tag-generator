import qrcode
import os.path
def generate_cute_qr(qrpath,data):
    from PIL import Image, ImageDraw, ImageFont

    heading = "A Hacker known as %s" % (data["owner"])
    emailtext = "Email: %s" %data["email"]
    twittertext= "Twitter: %s" %data["twitter"]
    urltext = "URL: %s" %data["url"]
    freitext = "%s"%data["text"]
    textOffset =0

    im = Image.open("../resources/A6_300dpi.png")
    qr = Image.open(qrpath)
    qr.convert('RGB')
    im.convert('RGB')
    headingFontsize = 70
    headingFont = ImageFont.truetype("../resources/arialbd.ttf", headingFontsize)
    textFontsize = 40
    textFont = ImageFont.truetype("../resources/arial.ttf", textFontsize)
    offsetX = 340  #offset for the shackspace logo on the leftside
    draw = ImageDraw.Draw(im)
    #Heading
    headingWidth, headingHeight = draw.textsize(heading, font=headingFont)
    draw.text((((im.size[0]- offsetX)/2) - (headingWidth/2 - offsetX), im.size[1]/8), heading, font=headingFont, fill="#000000")
    #Text
    textWidth, textHeight = draw.textsize(emailtext, font=textFont)
    draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), im.size[1]/5), emailtext, font=textFont, fill="#000000")
    textOffset += textHeight
    if data["twitter"]:
        draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), (im.size[1]/5)+textOffset), twittertext, font=textFont, fill="#000000")
        textOffset += textHeight
    if data["url"]:
        draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), (im.size[1]/5)+textOffset), urltext, font=textFont, fill="#000000")
        textOffset += textHeight
    if data["text"]: #add another line
        draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), (im.size[1]/5)+textOffset+textHeight), freitext, font=textFont, fill="#000000")

        #QR-Code
    draw.bitmap(((im.size[0]-offsetX)/2 - (qr.size[0]/2 - offsetX), im.size[1]/2.2), qr, fill="#000000")
    del draw
    im.save(qrpath, "PNG")