# MirraPy

Python用のMirattivAPIラッパー

## インストール

```bash
pip install mirrapy
```

## パッケージを更新する場合：

```bash
pip install --upgrade mirrapy
```



## 注意事項
> [!IMPORTANT]
> IP制限について: 一度に2つ以上のアカウントを作成すると、一時的にIPアドレスがロックされる場合がありますのでご注意ください。
> アカウント連携について: 現在の仕様上、端末が未確認と判定されるため、ログインにはアカウント連携が必要となります。

#### 使い方（サンプルコード）
```py
from MirraPy import Client, MirrativError
import httpx, asyncio

async def main():
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        try:
            client = Client(ac)
                
            #Profile情報取得
            profile_data = await client.util.get_profile(user_id="132628940")
            print("プロフィール名:", profile_data.user_name)
            print("フォロー数:", profile_data.follow)
            print("フォロワー数:", profile_data.follower)
            
            #ライブIDの取得
            print(await client.util.parse_url(url="シェアLinkをそのまま張り付けてOK")) #ライブIDを取得可能
            live_id = await client.util.get_liveID(user_id=119401577) #ユーザーIDからライブIDを取得可能
            print(live_id)
            
            client.live.set_liveid(live_id=live_id) #ライブIDを設定できる。柔軟にしたい場合は使わなくてもok
            check_live_info = await client.live.check_live() 
            
            #boolで返されます
            print("ライブ配信されているか:", check_live_info.alive)
            print("コラボ可能か:", check_live_info.is_collabo)
            
            await client.live.Collabo_Request() #コラボ通話のリクエスト
            await client.live.Collabo_Cancel() #コラボ通話のキャンセル
            await client.util.live_request(user_id=12345, count=9999) #ライブリクエスト countはリクエストする回数
            
        except MirrativError as e:
            print(e)
     
     
async def login_edit():
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        saved_mr_id = "RJW6oaI04zBZH8c91lzJ9vTityUyGvPqEPHLa8PLq1cP4SUpVM8SvOUkv19QPWvM" #ミラティブのID。これがないとログインできない。
        client = Client(ac)
        client.login(mr_id=saved_mr_id) #基本的には必要。アカウント作成時は必要なし。
        
        #Profile変更
        await client.user.edit_profile(name="テスト", description="説明文", url="指定のリンク")
        
async def create_ac():
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        client = Client(ac)
        
        #ミラティブアカウントの作成
        result = await client.user.create_account(name="テスト", description="説明文", url="任意のURL", save_mode=True) #作成したアカウントを保存するか。
        print(result.username) #ユーザー名
        print(result.userid) #ユーザーID
        print(result.mr_id) #ミラティブID これがないとログインできない

asyncio.run(main())
asyncio.run(login_edit())
asyncio.run(create_ac())
```

### 補足
Mirattivのログイン鍵があるのでログイン機能も追加予定。

### アカウントについて
現在の状況では端末が未確認とでる為アカウント連携が必須になる。

## コンタクト  
Discord: a
X: b


