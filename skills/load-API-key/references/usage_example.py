"""
usage_example.py
=================
shared_apikey_loader 사용 예제

의존성:
    pip install python-dotenv openai anthropic
"""

from shared_apikey_loader import load_shared_keys, get_key


def main():
    # 공용서버에서 API 키 로드
    load_shared_keys()

    # OpenAI API 사용 예시
    openai_key = get_key("OPENAI_API_KEY")
    if openai_key:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print(response.choices[0].message.content)

    # Anthropic API 사용 예시
    anthropic_key = get_key("ANTHROPIC_API_KEY")
    if anthropic_key:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        message = client.messages.create(
            model="claude-sonnet-4-6-20250627",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print(message.content[0].text)


if __name__ == "__main__":
    main()
