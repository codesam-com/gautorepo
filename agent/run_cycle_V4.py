from run_cycle import main as previous_cycle
from manual_cleanup_advisor import generate_cleanup_requests


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Generating manual cleanup requests...")
    requests = generate_cleanup_requests()

    for r in requests:
        print(r)


if __name__ == "__main__":
    main()
