import re
import os
import requests
def create_directory(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print("file alrady created")

create_directory("dimik_pub")
st = """  <div class="book-cover">

					 <a href="http://dimik.pub/book/439/kritikothon-story-of-tech-geniuses-by-tamanna-nishat-rini"><img src="http://dimik.pub/wp-content/uploads/2019/03/kriti-kothon-front-cover-350x450.jpg"></a>
                </div>

                <div class="slide-description">
                    <div class="inner-sd">
                        <div class="top-sd-head clearfix">
                            <div class="tsh-left">
                            <h2 class="sd-title"><a href="http://dimik.pub/book/439/kritikothon-story-of-tech-geniuses-by-tamanna-nishat-rini">কৃতিকথন : টেক জগতের জিনিয়াসদের কথা</a></h2>
                            </div>

"""

url = "http://dimik.pub/"
response = requests.get(url)
if response is False:
    print("url not found")
text = response.text
regexp = re.compile(r'<div class="book-cover">\s*<a href="(.*?)">\s*<img src="(.*?)">.*?<h2 class="sd-title"><.*?>(.*?)<',re.S)
result = re.findall(regexp,text)
for item in result:
    print("name:",item[2])
    print("image:", item[1])
    print("url:", item[0])
s ="http://dimik.pub/book/439/kritikothon-story-of-tech-geniuses-by-tamanna-nishat-rini"
result =[('30','programming','career')]
print(result[0])
li = list(result[0])
print(li)
dir_name = "_".join(li)
print(dir_name)
