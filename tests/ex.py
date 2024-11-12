import random

scores = [random.randint(0, 100) for _ in range(50)]

print("<번호 순으로 출력")
print(scores)

scores.sort(reverse=True)

print("<성적 순으로 출력")
print(scores)

avg = sum(scores) / len(scores)

print(f"-> 전체 평점: {avg: .02f}")

high_scores = scores[:10]
print(f"상위 10명의 점수: {high_scores}")
avg_high = sum(high_scores) / len(high_scores)
print(f"상위 10명의 평점: {avg_high: .02f}")

low_scores = scores[-10:]
print(f"하위 10명 평점: {low_scores}")
avg_low = sum(low_scores) / len(low_scores)
print(f"하위 10명의 평점: {avg_low: .02f}")