from prisma import Prisma

prisma = Prisma()


async def get_words(user_name: str):
    await prisma.connect()

    text = await prisma.text.find_first(
        where={"userName": user_name},
        order={"date": "desc"}
    )
    text_id = text.id
    text_length = text.totalWords

    unknown_words = await prisma.words.find_many(
        where={"userName": user_name,
               "textId": text_id},
    )
    print(unknown_words)

    num_unknown = len([word.word for word in unknown_words]) if unknown_words else 0
    await prisma.disconnect()
    return num_unknown, text_length, text.level


async def update_user_level(user_name: str):
    # For text length and unknown words
    unknown_words, total_words, text_level = await get_words(user_name)

    await prisma.connect()
    user = await prisma.user.find_unique(where={"name": user_name})
    old_level = user.level
    new_level = max(update_score(total_words, unknown_words, old_level, text_level), 0)
    print('old level:', old_level)
    print('new level:', new_level)
    await prisma.history.create(data={
        "level": new_level,
        "language": user.language,
        "userName": user.name,
    })
    # For level and level average
    levels = await prisma.history.find_many(
        where={"userName": user_name},
        order={"date": "desc"},
        take=20
    )
    levels.sort(key=lambda hist: hist.level)
    new_average_level = max(sum(level.level for level in levels[:min(len(levels), 8)]) / len(levels), 0.1)
    print('new average level:', new_average_level)
    updated_user = await prisma.user.update(
        where={"name": user.name},
        data={"level": new_average_level}
    )

    await prisma.disconnect()
    return old_level, new_average_level


def update_score(tot_words, unknown_words, user_level, txt_lvl):
    learning_rate = 100

    compr_rate = 1 - (unknown_words / tot_words)
    adjust = learning_rate * (compr_rate - 0.965) * txt_lvl
    new_level = user_level + adjust
    return new_level

    adjust = compr_rate - avg
    level = 0
    if 0.95 <= compr_rate <= 0.98:
        adjust = 0.01
    if 0.98 < avg:
        level += 0.1
    elif avg < 0.95:
        level -= 0.1
    adjust = adjust + level
    return adjust

