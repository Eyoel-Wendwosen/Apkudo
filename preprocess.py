import sys
import os

def preprocess(file_path): 
    try: 
        # try reading the file
        file = open(file_path, "r")
        
        # varialbes needed for preprocessing the whole file 
        validEvents = {"SEND", "RECV"}
        invalidRecord = []
        inventory = {}
        faultCodeList= {}
        
        # details about the current device in processing pipeline 
        recordIdx = 0
        currentRecordInvalid = False
        currentDeviceId = ""

        # read first line 
        line = ""
        while line != None:
            # read lines 
            line = file.readline()

            # if line is empty -> EOF break
            if line == "":
                break

            # udpate currentRecord index and invalid record flag
            if line == '\n':
                recordIdx += 1
                currentRecordInvalid = False
                continue

            # split words 
            words = line.strip().split(" ")
            
            # if size of words is 3 -> process event information 
            if (len(words) == 3):
                eventType, IMIE, SKU = words
                
                if eventType not in validEvents: 
                    invalidRecord.append((recordIdx, "Invalid Event",  eventType) )
                    currentRecordInvalid = True

                if not validateIMIENumber(IMIE):
                    invalidRecord.append((recordIdx, "Invalid IMIE", IMIE))
                    currentRecordInvalid = True
                
                currentDeviceId = IMIE
                inventory[currentDeviceId] = {
                    "status": eventType,
                    "SKU": SKU
                }
                recordIdx += 1

            # if size of words is 2 -> process device(fault) about current device 
            elif len(words) == 2:
                if currentRecordInvalid: 
                    continue

                faultCode, faultDescription = words 
                faultCodeList[faultCode] = faultDescription
                
                device = inventory[currentDeviceId]
                if "fault" not in device:
                    device["fault"] = []
                device["fault"].append((faultCode, faultDescription))
            
            # read next line
            line = file.readline()
            if line == "":
                break
                    
        remainingInventory = {}
        for IMIE, device in inventory.items(): 
            if device["status"] == "RECV":
                if device["SKU"] not in remainingInventory:
                    remainingInventory[device["SKU"]] = 1
                else: 
                    remainingInventory[device["SKU"]] += 1
        
        for SKU, device in remainingInventory.items(): 
            print(SKU, device)
        
        for record in invalidRecord: 
            print(record)
        
        for fault, desc in faultCodeList.items(): 
            print(fault, desc)

    except:
        print("Some Error Occured")
    finally: 
        # close file 
        file.close()


def validateIMIENumber(num): 

    n = len(num)
    # check the lenght of the number
    if n != 15:
        return False
    # use the Luhn Algorithm to check the validity of the number
    odd_digits = num[-1::-2]
    even_digits = num[-2::-2]
    checkSum = sum([int(d) for d in odd_digits])
    for dig in even_digits:
        d = int(dig)
        if d > 4:
            checkSum += (2 * d) - 9
        else: 
            checkSum += 2 * d
    
    return checkSum % 10 == 0



if __name__ == '__main__':
    if len(sys.argv) != 2: 
        print("To run program use: python preprocess.py <file_path>")
        sys.exit()

    file_path = sys.argv[1]
    if not os.path.exists(file_path): 
        print("Given file <" + file_path + "> doesn't exist! Please make sure the file exists.")
        sys.exit()

    # file_path = "file.txt"
    preprocess(file_path)
