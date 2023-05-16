import openai

openai.api_key = "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"
# id,object,created, model, usage[ 'prompt_tokens', 'completion_tokens', 'total_tokens']
# key 값들: id, object, created, model, usage , choices
# usage 랑 choices


# messages = [
#     {"role": "system", "content": "너는 나의 애인이야.."},
#     {"role": "user", "content": "점심 뭐먹을까"},
# ]

messages = []

while True:
    user_content = input("user : ")
    messages.append({"role" : "user", "content" : f"{user_content}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    print(completion['usage'])
    response = completion.choices[0].message['content'].strip()
    messages.append({"role" : "assistant", "content": f"{response}"})

    print(f"지피티쿤: {response}")