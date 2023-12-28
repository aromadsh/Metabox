from pydub import AudioSegment

src = "./answer.mp3"
dst = "./answer_test.wav"

audSeg = AudioSegment.from_mp3(src)
audSeg.export(dst, format="wav")