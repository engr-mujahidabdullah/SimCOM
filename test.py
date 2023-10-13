from data_check import CRC16

x = CRC16()
print(x.generate_crc16(0x0301000000010DCC))

def switch_case(option):
    switch_dict = {
        1: "Case 1",
        2: "Case 2",
        3: "Case 3",
        4: "Case 4",
        5: "Case 5",
        6: "Case 6",
        7: "Case 7",
        8: "Case 8",
        9: "Case 9",
        10: "Case 10",
        11: "Case 11",
        12: "Case 12",
        13: "Case 13",
        14: "Case 14",
        15: "Case 15"
    }

    return switch_dict.get(option, "Invalid Case")

# Example usage:
choice = 7
result = switch_case(choice)
print(result)
