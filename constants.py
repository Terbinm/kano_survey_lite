# constants.py

# KANO 分類的顏色和描述設定
KANO_SETTINGS = {
    'A': {
        'name': 'Attractive',
        'description': '魅力品質 - 提供時會令顧客滿意，但不提供也不會不滿意',
        'color': 'green',  # Tailwind 顏色
        'text_color': 'text-green-600',
        'bg_color': 'bg-green-500',
        'hover_color': 'hover:bg-green-600'
    },
    'O': {
        'name': 'One-dimensional',
        'description': '一維品質 - 提供時會令顧客滿意，不提供會令顧客不滿意',
        'color': 'blue',
        'text_color': 'text-blue-600',
        'bg_color': 'bg-blue-500',
        'hover_color': 'hover:bg-blue-600'
    },
    'M': {
        'name': 'Must-be',
        'description': '必要品質 - 提供時顧客視為理所當然，不提供會令顧客不滿意',
        'color': 'red',
        'text_color': 'text-red-600',
        'bg_color': 'bg-red-500',
        'hover_color': 'hover:bg-red-600'
    },
    'I': {
        'name': 'Indifferent',
        'description': '無差異品質 - 提供與否都不會影響顧客滿意度',
        'color': 'rose',
        'text_color': 'text-rose-300',
        'bg_color': 'bg-rose-200',
        'hover_color': 'hover:bg-rose-300'
    },
    'R': {
        'name': 'Reverse',
        'description': '反向品質 - 提供反而會令顧客不滿意',
        'color': 'yellow',
        'text_color': 'text-yellow-600',
        'bg_color': 'bg-yellow-500',
        'hover_color': 'hover:bg-yellow-600'
    },
    'Q': {
        'name': 'Questionable',
        'description': '可疑結果 - 問卷回答可能有誤',
        'color': 'purple',
        'text_color': 'text-purple-600',
        'bg_color': 'bg-purple-500',
        'hover_color': 'hover:bg-purple-600'
    }
}

# 為了方便在模板中使用，創建一些輔助字典
KANO_COLORS = {k: v['color'] for k, v in KANO_SETTINGS.items()}
KANO_TEXT_COLORS = {k: v['text_color'] for k, v in KANO_SETTINGS.items()}
KANO_BG_COLORS = {k: v['bg_color'] for k, v in KANO_SETTINGS.items()}
KANO_DESCRIPTIONS = {k: v['description'] for k, v in KANO_SETTINGS.items()}