from MirraPy import Client, MirrativError
import httpx, asyncio

async def main():
    #httpクライアントを設定する必要あり
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as ac:
        try:
            client = Client(ac)
                
            #Profile情報取得
            profile_data = await client.util.get_profile(user_id="132628940")
            print("プロフィール名:", profile_data.user_name)
            print("フォロー数:", profile_data.follow)
            print("フォロワー数:", profile_data.follower)
            
            print(await client.util.parse_url(url="https://www.mirrativ.com/deep_link_preview?link=https%3A%2F%2Fws9f.adj.st%2Flive%2FZsXinosWvRynUJpNgfRdYg%3Fadj_deep_link%3Dmirr%3A%2F%2F%2Flive%2FZsXinosWvRynUJpNgfRdYg%3Fwhere%3Dplayer_viewer_list%26adj_fallback%3Dhttps%3A%2F%2Fwww.mirrativ.com%2Flive%2FZsXinosWvRynUJpNgfRdYg%26adj_og_description%3D%E3%80%90%E3%82%B9%E3%83%A9%E3%82%B3%E3%83%AD%E3%80%91%E9%87%91%E3%83%96%E3%83%AB%E5%87%BA%E3%81%99%E3%81%9F%E3%81%B31000%26%E4%BB%8A%E6%9C%88%E4%B8%AD%E3%81%AE%E3%83%81%E3%82%A2%E3%83%AA%E3%81%A71500%E9%82%84%E5%85%83%E2%9C%A8%E4%B9%BE%E6%9D%AF%F0%9F%8D%BB%26adj_og_image%3Dhttps%3A%2F%2Fcdn.mirrativ.com%2Fmirrorman-prod%2Fimage%2Fcustom_thumbnail%2F59dcfd56ff46faf40c3e67ef9b0384aa40b738f5519d0db3aa2a6ca829a51924_share.jpeg%3F1788098639%26adj_og_title%3D%E3%81%86%E3%81%BF%E3%81%AD%E3%81%93%26adj_redirect_macos%3Dhttps%3A%2F%2Fwww.mirrativ.com%2Flive%2FZsXinosWvRynUJpNgfRdYg%26adj_t%3D1pkihi8s_1pyfvurh%26where%3Dplayer_viewer_list"))
        except MirrativError as e:
            print(e)
        
asyncio.run(main())