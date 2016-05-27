function descriptor()
   return {
      title = "Kanraoke",
      version = "0.1",
      shortdesc = "Kanraoke 0.1";
      capabilities = { "playing-listener",  "input-listener",  "meta-listener" }
   }
end

function activate()
   vlc.msg.info("[Kanraoke] Activated")
end

function deactivate()
   vlc.msg.info("[Kanraoke] Deactivated")
end

function playing_changed()
   return false
end

function input_changed()
   vlc.msg.info("[Kanraoke] Input changed ")
   local pl = vlc.playlist.get("playlist", false).children
   -- vlc.msg.info("Playlist items")
   -- for i, v in pairs(pl) do
      -- vlc.msg.info(v.name)
      -- vlc.msg.info(v.id)
      -- vlc.msg.info(v.nb_played)
   -- end
   if vlc.input.is_playing() then
      for i, v in pairs(pl) do
         if v.nb_played > 0 and v.id ~= vlc.playlist.current() then
            vlc.msg.info(v.name)
            vlc.msg.info(v.id)

            vlc.playlist.delete(v.id)
         end
      end
      -- vlc.msg.info("playing")
      -- local cur = vlc.input.item()
      -- vlc.msg.info("current playing")
      -- vlc.msg.info(vlc.playlist.current())
      -- vlc.msg.info("current playing")
      -- vlc.msg.info(cur:name())
      -- vlc.msg.info(cur:id())
   else
      for i, v in pairs(pl) do
         if v.nb_played > 0 then
            vlc.playlist.delete(v.id)
         end
      end
   end
end

function meta_changed()
   return false
end