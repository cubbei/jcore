import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--number', '-n', help="version number", type=str, required=True)
parser.add_argument('--message', '-m', help="message to add to text", type= str,required=True)
parser.add_argument('--webhook', '-w', help="webhook to post message to", type= str, required=True)

args=parser.parse_args()


body = {
    "content": "An update to the J-Core twitch Bot Framework has been released",
    "embeds":
        [
            {
                "title": "J-Core Update",
                "description": f"The J-Core framework has been updated to version **{args.number}**. View further details about jcore on PyPi.\n\n**Commit Details**: {args.message}",
                "url": "https://pypi.org/project/jcore/",
                "footer": 
                {
                    "text": f"J-Core v{args.number} | Jarvis by Cubbei"
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
