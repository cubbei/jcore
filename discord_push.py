import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--number', '-n', help="version number", type=str, required=True)
parser.add_argument('--message', '-m', help="message to add to text", type= str,required=True)
parser.add_argument('--webhook', '-w', help="webhook to post message to", type= str, required=True)

args=parser.parse_args()

if args.number == "" or args.number is None: 
    raise Exception("No version number provided")
if args.message == "" or args.message is None: 
    raise Exception("No build message provided")



body = {
    "content": "A new version of the JarvisCore package has been released",
    "embeds":
        [
            {
                "title": "Jarvis Core Update",
                "description": f"The Jarvis Core has been updated to version **{args.number}**. View further details about the Core on PyPi.\n\n**Commit Details**: {args.message}",
                "url": "https://pypi.org/project/jarviscore/",
                "footer": 
                {
                    "text": f"JarvisCore v{args.number} | Jarvis by Cubbei"
                }
            }
        ]
    }



response = requests.post(
    url=args.webhook,
    json=body
)

print("CODE: ", response.status_code)
print("Response Text: \n", response.text)
