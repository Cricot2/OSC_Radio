-- OSC RADIO
-- K2 play selected station.
-- K3 stop radio.
-- E2 select station.

local port = 5000
local ip = "192.168.1.105"
local dest = {ip, port}
local number = 4
local station = ""
local volume = 45
local volume_hp = 127
local volume_line = 120
local state_button = "Playing"
local default_font = 8
local mode = 0
local enc_len = 0

function init()
  mode = 0
  station_name()
  norns.encoders.set_sens(2, 16)
end

function redraw()
  if mode == 0 then
    mode1_ui()
    enc_len = 0
  elseif mode == 1 then
    mode2_ui()
    enc_len = 0
  end
end

function station_name()
  if number == 0 then
    station = "Canut"
  elseif number == 1 then
    station = "Musique"
  elseif number == 2 then
    station = "Info"
  elseif number == 3 then
    station = "Inter"
  elseif number == 4 then
    station = "Culture"
  elseif number == 5 then
    station = "FIP"
  end
end

function mode1_ui()
  screen.clear()
  screen.level(6)
  screen.move(1, 12)
  screen.font_size(12)
  screen.font_face(4)
  screen.text("OSC RADIO")
  screen.font_face(1)
  screen.font_size(default_font)
  screen.move(75, 12)
  screen.level(2)
  screen.text("> " .. state_button .. " <")
  screen.level(6)
  ui_deco()
  screen.move(1, 48)
  screen.level(2)
  screen.text("Station :  ")
  screen.level(6)
  screen.font_face(5)
  screen.font_size(14)
  screen.text(station)
  screen.level(6)
  screen.font_face(0)
  screen.font_size(default_font)
  screen.move(95, 60)
  screen.text("Vol : ")
  screen.text(volume)
  screen.update()
end

function mode2_ui()
  screen.clear()
  screen.level(6)
  screen.move(1, 12)
  screen.font_size(12)
  screen.font_face(4)
  screen.text("Sound Card")
  screen.font_size(default_font)
  screen.font_face(1)
  screen.level(2)
  screen.text("    < Volume >")
  ui_deco()
  screen.font_face(1)
  screen.font_size(default_font)
  screen.move(1, 60)
  screen.text("Vol Line: ")
  screen.text(volume_line)
  screen.move(80, 60)
  screen.text("Vol HP: ")
  screen.text(volume_hp)
  screen.update()
end

function ui_deco()
  screen.move(1, 26)
  screen.level(3)
  screen.line_width(12)
  screen.line_rel(128, 0)
  screen.stroke()
  screen.move(50, 29)
  screen.level(0)
  if mode == 0 then
    screen.move(4, 29)
    screen.text("<<<<<")
  else
    screen.text("              >>>>>")
  end
  screen.level(6)
  screen.update()
end

function key(n, z)
  if n == 3 and z == 1 then
    osc.send(dest, "/play", {number})
    state_button = "Playing"
  elseif n == 2 and z == 1 then
    osc.send(dest, "/stop", {1})
    state_button = "Stopped"
  end
  redraw()
end

function enc(n, d)
  if mode == 0 then
    if n == 2 then
      number = util.clamp(number + d, 0, 5)
      station_name()
    end

    if n == 3 then
      volume = util.clamp(volume + d, 0, 130)
      osc.send(dest, "/vol", {volume})
    end
    redraw()
  end

  if mode == 1 then
    if n == 2 then
      volume_line = util.clamp(volume_line + d, 0, 127)
      osc.send(dest, "/headphones", {volume_line})
    elseif n == 3 then
      volume_hp = util.clamp(volume_hp + d, 0, 127)
      osc.send(dest, "/speakers", {volume_hp})
    end
    redraw()
  end

  -- Interface switch
  if n == 1 then
    enc_len = (enc_len + d)
    if enc_len == 1 then
      mode = 1
    elseif enc_len == -1 then
      mode = 0
    end
    redraw()
  end
end
