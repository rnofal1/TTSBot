# ToDo: Replace this with a more intuitive system

# Standard
import argparse

# Local
import helpers.data as data


class AdminTools():
    def __init__(self):
        self.data = data.Data()

    def show_elevenlabs_alloc(self, args):
        print(self.data.open_pickle())

    def reset_elevenlabs_alloc(self, args):
        self.data.reset_elevenlabs_allocation(user_id=args.user_id)

    def set_elevenlabs_alloc(self, args):
        self.data.set_elevenlabs_allocation(user_id=args.user_id, num_chars=args.num_chars)

    def add_to_elevenlabs_alloc(self, args):
        self.data.add_to_elevenlabs_allocation(user_id=args.user_id, num_chars=args.num_chars)

    def subtract_from_elevenlabs_alloc(self, args):
        self.data.subtract_from_elevenlabs_allocation(user_id=args.user_id, num_chars=args.num_chars)

    
def main():
    admin_tools = AdminTools()

    # Setup main parser
    parser = argparse.ArgumentParser(description="Admin tools to control your data")
    subparsers = parser.add_subparsers(required=True)

    # Setup sub-parsers
    parser_show = subparsers.add_parser("show_elevenlabs_alloc")
    parser_show.set_defaults(func=admin_tools.show_elevenlabs_alloc)

    parser_reset = subparsers.add_parser("reset_elevenlabs_alloc")
    parser_reset.add_argument('user_id', type=int)
    parser_reset.set_defaults(func=admin_tools.reset_elevenlabs_alloc)

    parser_set = subparsers.add_parser("set_elevenlabs_alloc")
    parser_set.add_argument('user_id', type=int)
    parser_set.add_argument('num_chars', type=int)
    parser_set.set_defaults(func=admin_tools.set_elevenlabs_alloc)

    parser_add_to = subparsers.add_parser("add_to_elevenlabs_alloc")
    parser_add_to.add_argument('user_id', type=int)
    parser_add_to.add_argument('num_chars', type=int)
    parser_add_to.set_defaults(func=admin_tools.add_to_elevenlabs_alloc)

    parser_subtract_from = subparsers.add_parser("subtract_from_elevenlabs_alloc")
    parser_subtract_from.add_argument('user_id', type=int)
    parser_subtract_from.add_argument('num_chars', type=int)
    parser_subtract_from.set_defaults(func=admin_tools.subtract_from_elevenlabs_alloc)

    # Execute appropriate function + arguments
    args = parser.parse_args()
    args.func(args)
    

if __name__ == "__main__":
    main()
