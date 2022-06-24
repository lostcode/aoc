from typing import List


def get_padded_packet(hex_packet_str):
    hex_packet_len = len(hex_packet_str) - 2
    return format(int(hex_packet_str, 16), '0{}b'.format(hex_packet_len * 4))


def get_version(packet_bit_str: str, offset):
    end_pos = offset + 3
    return int(packet_bit_str[offset:end_pos], 2), end_pos


def get_type_id(packet_bit_str: str, offset):
    end_pos = offset + 3
    return int(packet_bit_str[offset:end_pos], 2), end_pos


def get_length_type_ID(packet_bit_str: str, offset):
    end_pos = offset + 1
    return int(packet_bit_str[offset:end_pos], 2), end_pos


def get_total_length(packet_bit_str: str, offset):
    end_pos = offset + 15
    return int(packet_bit_str[offset:end_pos], 2), end_pos


def get_num_sub_packets(packet_bit_str: str, offset):
    end_pos = offset + 11
    return int(packet_bit_str[offset:end_pos], 2), end_pos


def get_has_next_group(packet_bit_str, offset):
    end_pos = offset + 1
    return int(packet_bit_str[offset:end_pos], 2), end_pos


def get_literal_bit_str(packet_bit_str, offset):
    end_pos = offset + 4
    return packet_bit_str[offset:end_pos], end_pos


class Packet:
    version: int
    type_id: int
    sub_packets: List['Packet']
    literal: int
    bit_str: str

    def __init__(self, offset) -> None:
        self.offset = offset
        self.version = -1
        self.type_id = -1
        self.literal = -1
        self.sub_packets = []

    def __repr__(self) -> str:
        return 'Packet(offset={}, version={}, type_id={}, literal={}, sub_packets={})'.format(
            self.offset, self.version, self.type_id, self.literal, self.sub_packets
        )


def decode_packet(packet_bit_str, offset):
    packet = Packet(offset)
    packet.version, offset = get_version(packet_bit_str, offset)
    packet.type_id, offset = get_type_id(packet_bit_str, offset)

    if packet.type_id != 4:
        # operator packet
        length_type_id, offset = get_length_type_ID(packet_bit_str, offset)
        if length_type_id == 0:
            # packet length
            total_length, offset = get_total_length(packet_bit_str, offset)
            start_offset = end_offset = offset
            while end_offset - start_offset < total_length:
                sub_packet, offset = decode_packet(packet_bit_str, offset)
                end_offset = offset
                packet.sub_packets.append(sub_packet)
        else:
            # number of packets
            num_sub_packets, offset = get_num_sub_packets(packet_bit_str, offset)
            for i in range(num_sub_packets):
                sub_packet, offset = decode_packet(packet_bit_str, offset)
                packet.sub_packets.append(sub_packet)
    else:
        # literal packet
        has_more_groups, offset = get_has_next_group(packet_bit_str, offset)

        literal_str = ''
        while has_more_groups != 0:
            this_literal_str, offset = get_literal_bit_str(packet_bit_str, offset)
            literal_str += this_literal_str
            has_more_groups, offset = get_has_next_group(packet_bit_str, offset)

        this_literal_str, offset = get_literal_bit_str(packet_bit_str, offset)
        literal_str += this_literal_str
        packet.literal = int(literal_str, 2)
        return packet, offset

    return packet, offset


def get_version_sum(packet):
    version_sum = packet.version
    for sub_packet in packet.sub_packets:
        version_sum += get_version_sum(sub_packet)
    return version_sum


def get_value(packet: Packet):
    if packet.type_id == 0:
        # sum packet
        value = sum([get_value(sub_packet) for sub_packet in packet.sub_packets])
    elif packet.type_id == 1:
        # product packet
        from math import prod
        value = prod([get_value(sub_packet) for sub_packet in packet.sub_packets])
    elif packet.type_id == 2:
        # minimum packet
        value = min([get_value(sub_packet) for sub_packet in packet.sub_packets])
    elif packet.type_id == 3:
        # maximum packet
        value = max([get_value(sub_packet) for sub_packet in packet.sub_packets])
    elif packet.type_id == 4:
        # literal packet
        value = packet.literal
    elif packet.type_id == 5:
        # greater than packet
        assert len(packet.sub_packets) == 2
        value = 1 if get_value(packet.sub_packets[0]) > get_value(packet.sub_packets[1]) else 0
    elif packet.type_id == 6:
        # less than packet
        assert len(packet.sub_packets) == 2
        value = 1 if get_value(packet.sub_packets[0]) < get_value(packet.sub_packets[1]) else 0
    elif packet.type_id == 7:
        # equal to packet
        assert len(packet.sub_packets) == 2
        value = 1 if get_value(packet.sub_packets[0]) == get_value(packet.sub_packets[1]) else 0

    return value


# hex_packet = '0xD2FE28'
# hex_packet = '0x38006F45291200'
# hex_packet = '0xEE00D40C823060'
# hex_packet = '0x8A004A801A8002F478'
# hex_packet = '0x620080001611562C8802118E34'
# hex_packet = '0xC0015000016115A2E0802F182340'
# hex_packet = '0xA0016C880162017C3686B18A3D4780'

# hex_packet = '0xC200B40A82'
# hex_packet = '0x04005AC33890'
# hex_packet = '0x880086C3E88112'
# hex_packet = '0xCE00C43D881120'
# hex_packet = '0xD8005AC2A8F0'
# hex_packet = '0xF600BC2D8F'
# hex_packet = '0x9C005AC2F8F0'
# hex_packet = '0x9C0141080250320F1802104A08'

hex_packet = '0x0054FEC8C54DC02295D5AE9B243D2F4FEA154493A43E0E60084E61CE802419A95E38958DE4F100B9708300466AB2AB7D80291DA471EB9110010328F820084D5742D2C8E600AC8DF3DBD486C010999B44CCDBD401C9BBCE3FD3DCA624652C400007FC97B113B8C4600A6002A33907E9C83ECB4F709FD51400B3002C4009202E9D00AF260290D400D70038400E7003C400A201B01400B401609C008201115003915002D002525003A6EB49C751ED114C013865800BFCA234E677512952E20040649A26DFA1C90087D600A8803F0CA1AC1F00042A3E41F8D31EE7C8D800FD97E43CCE401A9E802D377B5B751A95BCD3E574124017CF00341353E672A32E2D2356B9EE79088032AF005E7E8F33F47F95EC29AD3018038000864658471280010C8FD1D63C080390E61D44600092645366202933C9FA2F460095006E40008742A8E70F80010F8DF0AA264B331004C52B647D004E6EEF534C8600BCC93E802D38B5311AC7E7B02D804629DD034DFBB1E2D4E2ACBDE9F9FF8ED2F10099DE828803C7C0068E7B9A7D9EE69F263B7D427541200806582E49725CFA64240050A20043E25C148CC600F45C8E717C8010E84506E1F18023600A4D934DC379B9EC96B242402504A027006E200085C6B8D51200010F89913629A805925FBD3322191A1C45A9EACB4733FBC5631A210805315A7E3BC324BCE8573ACF3222600BCD6B3997E7430F004E37CED091401293BEAC2D138402496508873967A840E00E41E99DE6B9D3CCB5E3F9A69802B2368E7558056802E200D4458AF1180010A82B1520DB80212588014C009803B2A3134DD32706009498C600664200F4558630F840188E11EE3B200C292B59124AFF9AE6775ED8BE73D4FEEFFAD4CE7E72FFBB7BB49005FB3BEBFA84140096CD5FEDF048C011B004A5B327F96CC9E653C9060174EA0CF15CA0E4D044F9E4B6258A5065400D9B68'

padded_packet = get_padded_packet(hex_packet)
packet, offset = decode_packet(padded_packet, 0)
print(get_version_sum(packet))

print(get_value(packet))

