from lxml import html, etree
import sys
import io
import codecs

# sys.setdefaultencoding("utf-8")
input_file = str(sys.argv[1])
output_file = str(sys.argv[2])
myfile = codecs.open(input_file,'r','utf-8')
output_file = codecs.open(output_file,'w','utf-8')
# myfile = open('result2.html','r')
# output_file = open('result2.xml','w')
html_page = myfile.read()

doc = etree.HTML(html_page)

output_dictionary = {}

results_list = doc.xpath('//ul[@id = "s-results-list-atf"]/li/@id')
# results_li = doc.xpath('//ul[@id = "s-results-list-atf"]/li[@id="result_12" and @data-asin="1786462966"]//h2/text()')

data_asin = doc.xpath('//ul[@id = "s-results-list-atf"]/li/@data-asin')

# print(results_list)
for i in range(0,len(results_list)):
    output_dictionary[i] =[]

for key,value in output_dictionary.items():
    #Book Title
    book_title = doc.xpath('//*[@id="'+results_list[key]+'" and @data-asin="'+data_asin[key]+'"]//h2[@data-attribute]/text()')
    #Author
    a1 = doc.xpath('//*[@id="'+results_list[key]+'" and @data-asin="'+data_asin[key]+'"]/div/div/div/div[2]/div[2]/div[2]/span/text()')
    a2 = doc.xpath('//*[@id="'+results_list[key]+'" and @data-asin="'+data_asin[key]+'"]/div/div/div/div[2]/div[1]/div[2]/span/text()')
    a5 = doc.xpath('//*[@id="'+results_list[key]+'" and @data-asin="'+data_asin[key]+'"]/div/div/div/div[2]/div[1]/div[2]/span/a/text()')
    
    author_or = a1+a2+a5

    for i in range(0,len(author_or)):
        author_or[i] = author_or[i].strip()

    for i in range(len(author_or) - 1, -1, -1):
        if author_or[i]=='by' or author_or[i]=='and':
            del author_or[i]

    for i in range(0,len(author_or)):
        if 'and' in author_or[i]:
            author_or[i] = author_or[i].replace('and','')
        if 'by' in author_or[i]:
            author_or[i] = author_or[i].replace('by','')

    #Publication Year
    publication_year = []
    y1 = doc.xpath('//*[@id="'+results_list[key]+'" and @data-asin="'+data_asin[key]+'"]/div/div/div/div[2]/div[1]/div[1]/span[3]/text()')
    y2 = doc.xpath('//*[@id="'+results_list[key]+'" and @data-asin="'+data_asin[key]+'"]/div/div/div/div[2]/div[2]/div[1]/span[3]/text()')
    publication_year = y1+y2

    value.append(book_title)
    value.append(publication_year)
    value.append(author_or)
    

def checkRow(string):
    if '&' in string:
        string = string.replace('&','&amp;')
    if '<' in string:
        string = string.replace('<','&lt;')
    if '>' in string:
        string = string.replace('>','&gt;')
    if '\"' in string:
        string = string.replace('\"','&quot;')
    if '\'' in string:
        string = string.replace('\'','&apos;')
    return(string)

output_file.write('<books>\n')
for value in output_dictionary.values():
    if len(value[0]) == 0:
        continue
    output_file.write('\t<book>\n')
    for i in range(0,len(value[0])):
        output_file.write('\t\t<title>'+checkRow(value[0][i])+'</title>\n')
    for i in range(0,len(value[1])):
        output_file.write('\t\t<publication_date>'+checkRow(value[1][i])+'</publication_date>\n')
    for i in range(0,len(value[2])):
        output_file.write('\t\t<author>'+checkRow(value[2][i])+'</author>\n')
    output_file.write('\t</book>\n')
output_file.write('</books>')
