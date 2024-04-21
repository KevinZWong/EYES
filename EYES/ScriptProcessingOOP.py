import re


class ScriptProcessing:
    def __init__(self):
        pass
    def format_script(self, script, min_length):
        def segment_valid_check(segment, number):
            if len(segment.split(" ")) < number:
                return False
            return True

        caption_script = re.split(r'[.!?;]\s*', script)

        caption_script = [sentence for sentence in caption_script if sentence]
        print("caption_script", caption_script)
        final_caption_script = []
        segments_index = 0

        while segments_index < len(caption_script):
            segment_block = caption_script[segments_index]
            while not(segment_valid_check(segment_block, min_length)):
                
                segments_index += 1
                if segments_index == len(caption_script):
                    break
                segment_block += " " + caption_script[segments_index]
            final_caption_script.append(segment_block)
            segments_index += 1

        return final_caption_script


if __name__ == "__main__":    
    obj = ScriptProcessing()
    script = """segment1. segment2. segment3 a a a a a a. a a a a a a a a a a. segment1. segment2. segment3 a a a a a a. a a a a a a a a a a. 
    """
    print(obj.format_script(script))


