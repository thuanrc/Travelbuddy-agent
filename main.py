import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

from travelbuddy.agents.agent import graph


def main():
    print("=" * 60)
    print("  TravelBuddy - Tro ly Du lich Thong minh")
    print("  Go 'quit' de thoat")
    print("=" * 60)
    print()

    # Luu lich su chat giua cac vong
    chat_history = []

    while True:
        try:
            user_input = input("\nBan: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nTam biet! Chuc ban nhung chuyen di vui ve!")
                break

            # Them tin nhan moi vao lich su
            chat_history.append(("human", user_input))

            print("\nTravelBuddy dang suy nghi...")
            result = graph.invoke({"messages": chat_history})

            # Lay response moi nhat
            final = result["messages"][-1]

            # Them response vao lich su de giu context
            chat_history.append(("ai", final.content))

            print(f"\nTravelBuddy: {final.content}")

        except KeyboardInterrupt:
            print("\n\nTam biet! Chuc ban nhung chuyen di vui ve!")
            break
        except Exception as e:
            print(f"\nLoi: {e}")


if __name__ == "__main__":
    main()
