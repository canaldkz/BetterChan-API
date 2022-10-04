from typing import Union

def clamp(num:Union[int, float], mn:Union[int, float], mx:Union[int, float]) -> Union[int, float]:
    return min(max(num, mn), mx)


if __name__ == "__main__":
    print(clamp(21, 10, 20))
    # print(get_preview_url('https://mimg4.imgschan.xyz/manganew_webp/n/1661801384_nekomata/003.webp'))