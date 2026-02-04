import asyncio
import sys
from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType

async def main():
    client = CopilotClient()
    await client.start()
    prompt = "短めの面白い話頼む"
    ans = await call_agent(client, prompt, "Client1")
    await client.stop()
    
    client2 = CopilotClient()
    await client2.start()
    prompt2 = f'''
    以下は日本語の面白い話です。感想を教えてください。
    \n
    {ans}
    '''
    await call_agent(client2, prompt2, "Client2")
    await client2.stop()
    

async def call_agent(client, prompt: str, client_name: str) -> str:
    print(f"--- {client_name} sending prompt ---")
    session = await client.create_session({
        "model": "gpt-5.2",
        "streaming": True
        })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()
        elif event.type == SessionEventType.SESSION_IDLE:
            print("\n--- Session is idle ---")
        elif event.type == SessionEventType.SESSION_ERROR:
            print(f"\n--- Session error: {event.data.error_message} ---")
            
    session.on(handle_event)
    try:
        response = await session.send_and_wait({"prompt": prompt})
        return response.data.content
    finally:
        await session.destroy()

asyncio.run(main())