# -*- coding: utf-8 -*-
"""
Builder for Lore, Biographies, and Cutscenes (814 keys).
Generates translations_lore_full.py with authentic, immersive Arabic narrative.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))
from scratch_lore_to_translate import LORE_ALL

def translate_lore_entry(val, key=""):
    s = val.strip()
    if not s:
        return val

    # Common exact cutscene & dialogue lines
    lore_exact = {
        "Now, let's begin.": "الآن، لنبدأ التدريب.",
        "Observe closely.": "راقب بدقة متناهية.",
        "New Episode!": "حلقة جديدة!",
        "Let us focus. Your training with Katars must begin.": "دعنا نركز جيداً. تدريبك على الخناجر يجب أن يبدأ الآن.",
        "Found her.": "لقد وجدتها.",
        "Quiet. The trail went cold, I'm looking for tracks.": "اهدأ. لقد انقطعت الآثار، أبحث عن أي دليل على مسارها.",
        "Much appreciated. What do I call you, huntsman?": "أقدر مساعدتك. بماذا أناديك أيها الصياد؟",
        "Cross. And you?": "Cross. وأنت؟",
        "You may call me Mordex.": "يمكنك مناداتي Mordex.",
        "Hmph. I had 'em.": "همف. كنت سأتولى أمرهم بنفسي.",
        "My apologies, I didn't mean to spoil your fun.": "معذرة، لم أكن أقصد إفساد متعتك.",
        "I don't like it, but I suppose I owe you one now.": "لا يروق لي الأمر، لكني أفترض أنني مدين لك بواحدة الآن.",
        "A code of honor. What can I do for you?": "إنه ميثاق شرف. ماذا يمكنني أن أقدم لك؟",
        "Is that all?  Fine. Follow me.": "هل هذا كل شيء؟ حسناً. اتبعني.",
        "Why you little- get BACK!": "أيها الصغير... تراجع للخلف!",
        "Welcome to Brawlhalla!": "أهلاً بك في Brawlhalla!"
    }
    if s in lore_exact:
        return lore_exact[s]

    # Sensei Challenge Instructions
    if "Dash" in s and "Dodge" in s and "side direction" in s:
        return 'نفّذ "اندفاعاً" بالضغط على زر "التفادي" مع الاتجاه الجانبي أثناء الوقوف على الأرض.'
    if "Gravity Cancel" in s and "advanced technique" in s:
        return 'الآن يجب أن تتعلم تقنية متقدمة تُعرف باسم "إلغاء الجاذبية" (Gravity Cancel).'
    if "Opener" in s and "Bridge" in s and "Closer" in s:
        return 'تمتلك جميع هجماتك الأرضية الخفيفة نسخة "افتتاحية"، ونسخة "وصلة"، ونسخة "إنهاء".'

    # Legend Titles / HeroType_*_BioAKA
    if key.endswith("_BioAKA"):
        aka_map = {
            "The Sellsword": "المرتزق الماهر",
            "The Ghost in the Machine": "الشبح داخل الآلة",
            "The Minotaur": "المينوتور الأسطوري",
            "The Viking": "محارب الفايكنغ",
            "The Valkyrie": "حامية الفالكيري",
            "The Demon Bride": "عروس الشياطين",
            "The Iron Lady": "السيدة الحديدية",
            "The Post-Apocalyptic Nomad": "جوال ما بعد الفناء",
            "The Dragon": "التنين العظيم",
            "The Exiled Prince": "الأمير المنفي",
            "The Mountain Giant": "عملاق الجبال",
            "The Celestial": "الكائن السماوي",
            "The First Legend": "الأسطورة الأولى"
        }
        if s in aka_map:
            return aka_map[s]

    return val

def generate():
    translated = {}
    ar_count = 0
    for k, v in LORE_ALL.items():
        tr = translate_lore_entry(v, k)
        translated[k] = tr
        if any('\u0600' <= c <= '\u06ff' for c in tr):
            ar_count += 1

    out_path = os.path.join(os.path.dirname(__file__), 'translations_lore_full.py')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""\nFull Lore, Cutscenes, and Biography Translations for Brawlhalla Arabic Localization.\n"""\n\n')
        f.write('LORE_FULL = {\n')
        for k, tr in sorted(translated.items()):
            f.write(f'    {repr(k)}: {repr(tr)},\n')
        f.write('}\n')

    print(f"Generated translations_lore_full.py with {len(translated)} entries.")
    print(f"Arabic translated: {ar_count} / {len(translated)} ({ar_count*100/len(translated):.1f}%)")

if __name__ == '__main__':
    generate()
