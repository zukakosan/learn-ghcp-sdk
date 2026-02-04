import asyncio
import sys
import os
from copilot import CopilotClient, define_tool
from copilot.generated.session_events import SessionEventType

@define_tool(description="Get files in a local directory")
async def list_local_files(directory: str = ".") -> str:
    """
    List all files in the specified directory.
    
    Args:
        directory: The directory path to list files from. 
                   Can be absolute path (e.g., /home/user/documents) 
                   or relative path (e.g., ../parent_dir)
                   Default is current directory.
    
    Returns:
        A newline-separated list of file names
    """
    try:
        expanded_path = os.path.expanduser(directory)
        files = os.listdir(expanded_path)
        return f"Files in {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error listing files in {directory}: {str(e)}"

async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session({
        "model": "gpt-4.1",
        "streaming": True,
        "tools":[list_local_files]
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
    response = await session.send_and_wait({
        "prompt": "このディレクトリのファイルを教えてください"
        })            
    print(response.data.content)
    await client.stop()

asyncio.run(main())

# how to use
# https://github.com/github/copilot-sdk/tree/main/python