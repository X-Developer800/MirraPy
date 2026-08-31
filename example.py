from MirraPy import Client, MirrativError
import httpx, asyncio

async def main():
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        try:
            client = Client(ac)
                
            #Profile情報取得
            profile_data = await client.user.profile(user_id="149955798")
            print("プロフィール名:", profile_data.user_name)
            print("フォロー数:", profile_data.follow)
            print("フォロワー数:", profile_data.follower)
            
            #ライブIDの取得
            live_id = await client.live.find_id(user_id_or_url=100394211) #ユーザーIDからライブIDを取得可能
            client.login(mr_id="rIf6lS7YSPAD-2gs0V-8VCeZvOQFN1FkjJfPZv14_7a2mapJbNSTlNgPoKMnATrt")
            print(live_id)
            
            client.set_liveid(live_id=live_id) #ライブIDを設定できる。柔軟にしたい場合は使わなくてもok
            check_live_info = await client.live.status()
            print("ライブ配信されているか:", check_live_info.alive)
            print("コラボ可能か:", check_live_info.collab_enabled)
            
            await client.collab.request() #コラボ通話のリクエスト
            await client.collab.cancel() #コラボ通話のキャンセル
            await client.user.live_request(user_id=12345, count=9999) #ライブリクエスト countはリクエストする回数
            
        except MirrativError as e:
            print(e)
            
async def login_edit():
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        saved_mr_id = "RJW6oaI04zBZH8c91lzJ9vTityUyGvPqEPHLa8PLq1cP4SUpVM8SvOUkv19QPWvM" #ミラティブのID。これがないとログインできない。
        client = Client(ac)
        client.login(mr_id=saved_mr_id) #基本的には必要。アカウント作成時は必要なし。
        
        #Profile変更
        await client.user.update_profile(name="テスト", description="説明文", url="指定のリンク")
        
async def create_ac():
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        client = Client(ac)
        
        #ミラティブアカウントの作成
        result = await client.user.create_account(name="テスト", description="説明文", url="任意のURL", save_mode=True) #作成したアカウントを保存するか。
        print(result.username) #ユーザー名
        print(result.userid) #ユーザーID
        print(result.mr_id) #ミラティブID これがないとログインできない
     
asyncio.run(main())
