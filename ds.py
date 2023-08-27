from ragdoll.django import env

MY_INT_SETTING = env.Int(name="YESINT")
MY_STR_SETTING = env.Str()
MY_BOOL_SETTING = env.Bool()
