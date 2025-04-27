from machline_wrapper import machline_wrapper

def main():
    input_file_path = "./half_wing_input/half_wing_input.json" #"./ext/MachLine/dev/input_files/half_wing_input.json"
    ml_out = machline_wrapper.run_machline(input_file_path)

    print(ml_out)

if __name__ == "__main__":
    main()