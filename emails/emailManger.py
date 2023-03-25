from email.message import EmailMessage
import ssl
import smtplib

class EmailManger:

    def __init__(self) -> None:
        self.files = {
            "resend": {
                "filename": "emails\\resendCode.txt",
                "subject": "Code Resend Request - TheEventHub",
                "code_pos": 4
            },
            "eventCreated": {
                "filename": "emails\eventCreated_Msg.txt",
                "subject": "Event Sucessfully Created - TheEventHub",
                "code_pos": 6
            }
        }
        
        self.passwd = "SRMemail@1234"
        self.sender = "ar7051@srmist.edu.in"
        
        self.context = ssl.create_default_context()
        self.email = EmailMessage()
        self.email["From"] = self.sender
    
    
    def getMessage(self, name:str, code:str, file:str):
        code_pos = self.files[file]["code_pos"]
        file_name = self.files[file]["filename"]
        with open(file_name, 'r') as f:
            lines = f.readlines()          
            lines[0] = lines[0].replace("[Recipient's Name]", name)
            lines[code_pos] = lines[code_pos].replace("[code here]", code)
        return ''.join(lines)
    
    def sendMail(self, reciever:str):
        with smtplib.SMTP_SSL(
            host='smtp.gmail.com', 
            port=465, 
            context=self.context
        ) as smtp:
            smtp.login(
                user=self.sender,
                password=self.passwd
            )
            smtp.sendmail(
                from_addr=self.sender,
                to_addrs=reciever,
                msg=self.email.as_string()
            )
    
    def sendSucessfullMail(
        self, 
        reciever: str, 
        deleteCode: str,
        userName: str,
    ):
        file = "eventCreated"
        self.email["To"] = reciever
        print(len(self.email["To"]))
        self.email["Subject"] = self.files[file]["subject"]
        body = self.getMessage(name=userName, code=deleteCode, file=file)          
        self.email.set_content(body)
        self.sendMail(reciever=reciever)
        
    def resendCodeRequest(
        self, 
        reciever: str, 
        deleteCode: str,
        userName: str,
    ):
        file = "resend"
        self.email["To"] = reciever
        self.email["Subject"] = self.files[file]["subject"]
        body = self.getMessage(name=userName, code=deleteCode, file=file)          
        self.email.set_content(body)
        self.sendMail(reciever=reciever)
        

if __name__ == "__main__":
    EmailManger()