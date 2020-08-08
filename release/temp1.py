import json
a = 1
with open('111','r') as file:
    for i in file.readlines():
        EMQTopic = i.split("\"")[3]
        KAFKATopic = i.split("\"")[7]
        print("SELECT clientid client_id,username,topic,qos,timestamp ts,node,base64_encode(payload) payload FROM \"%s\"" % (EMQTopic))
        print(KAFKATopic)
        print("\n")
        print(a)
        a = a + 1