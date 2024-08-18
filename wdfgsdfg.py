import datetime

import pandas as pd

from database import get_session, User
from lang_based_variable import Lang

dtype_dict = {
    'id': 'int64',
    'outbalance': 'Int64',
    'fc': 'float64',
    'ref': 'str',
    'regDate': 'str',
    'totalbonus': 'float64',
    'payout': 'float64',
    'userActivatedPromo': 'float64',
    'premium': 'float64',
    'ban': 'float64',
    'refCount': 'float64',
    'not': 'float64',
    'data': 'float64',
    'last_bonus_day': 'float64',
    'last_com_day': 'float64',
    'bonuscount': 'float64',
    'imgay': 'float64',
    'proverka': 'float64',
    'check': 'float64',
    'subs': 'float64',
    # Handle completedTasks and usedPromoCodes as object type initially
}

# Import the CSV with dtype specified

mongo_df = pd.read_csv('c90758_geckoshig_bot_2.users.csv', dtype=dtype_dict, low_memory=False)
mongo_df = mongo_df.drop_duplicates(subset='id', keep='first')
mongo_df = mongo_df.rename(columns={
    'id': 'telegram_id',
    'outbalance': 'balance',
    'ref': 'referred_by_id',
    'ban': 'blocked',
    'premium': 'is_premium',
    'regDate': 'created_at',
    # Map other columns if needed
})


mongo_df['balance'] = mongo_df['balance'].fillna(0).astype(int)
mongo_df['bmeme_balance'] = 0  # Default value
mongo_df['bmeme_balance'] = mongo_df['bmeme_balance'].astype(int)
mongo_df['is_premium'] = mongo_df['is_premium'].fillna(0).astype(bool)
mongo_df['is_bot_start_completed'] = True  # Default value
mongo_df['is_admin'] = False  # Default value
mongo_df['language'] = 'EN'  # Default language
mongo_df['deleted_at'] = None  # Default None for deleted_at
# mongo_df['referred_by_id'] = mongo_df['referred_by_id'].astype('Int64')
# mongo_df['referred_by_id'] = mongo_df['referred_by_id'].where(pd.isna(mongo_df['referred_by_id']), None)


def convert_na_to_none(value):
    # Check if value is NaN or NA and return None if true
    if pd.isna(value):
        return None
    return value


mongo_df = mongo_df.map(convert_na_to_none)

mongo_df = mongo_df[[
    'telegram_id',
    'balance',
    'bmeme_balance',  # Ensure this column exists
    'referred_by_id',
    'blocked',
    'language',
    'is_admin',
    'is_premium',
    'is_bot_start_completed',
    'created_at',
    'deleted_at'
]]
mongo_df = mongo_df[mongo_df['telegram_id'] > 10]
data = mongo_df.to_dict(orient='records')
print(data[0])

s = get_session()


def b(d) -> User:
    try:
        created_at = pd.to_datetime(d['created_at'], dayfirst=True)
    except Exception as e:
        created_at = datetime.datetime.now(datetime.UTC)
    try:
        referred_by_id = int(d['referred_by_id'])
    except Exception as e:
        referred_by_id = None


    return User(
        telegram_id=d['telegram_id'],
        balance=d['balance'],
        bmeme_balance=0,
        referred_by_id=referred_by_id,
        blocked=False,
        language=Lang.EN,
        is_admin=False,
        is_premium=d['is_premium'],
        is_bot_start_completed=True,
        created_at=created_at,
    )


data_to_insert = [b(d) for d in data]

# Use bulk_save_objects
s.bulk_save_objects(data_to_insert)
s.commit()
