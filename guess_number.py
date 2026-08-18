import random


def main():
    """猜数字游戏主函数。"""

    target = random.randint(1, 100)

    guess_count = 0

    print("=" * 40)
    print("欢迎来到猜数字小游戏！")
    print("我已经想好了一个 1~100 之间的数字，快来猜猜看吧！")
    print("=" * 40)

    while True:
        user_input = input("请输入你猜的数字（1~100）：").strip()
        try:
            guess = int(user_input)
        except ValueError:
            print("输入无效：请输入一个数字，例如 42。")
            continue 

        if guess < 1 or guess > 100:
            print("输入无效：数字必须在 1~100 之间哦。")
            continue

        guess_count += 1

        if guess < target:
            print("猜小了，再往大猜一点。")
        elif guess > target:
            print("猜大了，再往小猜一点。")
        else:
            print("=" * 40)
            print(f"恭喜你，猜对了！正确答案就是 {target}。")
            print(f"你一共猜了 {guess_count} 次。")
            print("=" * 40)
            break 
            
if __name__ == "__main__":
    main()
