import pandas as pd
import json
import json 
from pandas.io.json import json_normalize


invalidjsonlist=[]
invalidjlist = []
df1 = pd.DataFrame()
invaliddf = pd.DataFrame()
df = pd.read_excel("Input.xlsx")

count = 0
for i,row in df.iterrows():
	item = df.at[i,'PAYLOAD_DATA']
	payloadid =df.at[i,'PAYLOAD_ID'] 
	
	try:
		json_dict = json.loads(item)
	except:
		print 'Invalid JSON encountered for PAYLOAD_ID = ',payloadid
		invalidjsonlist.append(payloadid)
		invalidjlist.append(item)
		continue
	# print list(d.keys())
	# data = pd.DataFrame.from_dict(dfj, orient='index')
	# print pd.DataFrame(d["creditreport"])
	# print pd.DataFrame(d["creditreport"], columns=[x["label"] for x in d["fields"]])
	# print d1
	# print pd.io.json.json_normalize(d)

	# df = pd.concat([pd.DataFrame(json_dict), 
	#                 json_normalize(json_dict['nested_array_to_expand'])], 
	#                 axis=1).drop('nested_array_to_expand', 1)




	def flatten_json(y):
	    out = {}

	    def flatten(x, name=''):
	        if type(x) is dict:
	            for a in x:
	                flatten(x[a], name + a + '_')
	        elif type(x) is list:
	            i = 0
	            for a in x:
	                flatten(a, name + str(i) + '_')
	                i += 1
	        else:
	            out[name[:-1]] = x

	    flatten(y)
	    return out

	flat = flatten_json(json_dict)
	dfj= json_normalize(flat)
	newrecord = dfj
	df1=pd.concat([df1,newrecord])

invaliddf['INVALID_PAYLOAD_ID']= invalidjsonlist
invaliddf['INVALID_JSON']= invalidjlist

writer = pd.ExcelWriter('JSON_TO_EXCEL_Output.xlsx')
df1.to_excel(writer,'JSONDATA',index=False)
invaliddf.to_excel(writer,'INVALIDJSONLIST',index=False)
workbook = writer.book
worksheet= writer.sheets['JSONDATA']
worksheet1= writer.sheets['INVALIDJSONLIST']
worksheet.set_column('A:Z',50)
worksheet1.set_column('A:Z',50)
writer.save()

raw_input('*********************Hit Enter to Exit***********************')
print 'Exiting Tool....!!!!'







