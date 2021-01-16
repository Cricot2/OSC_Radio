-- OSC RADIO
-- K2 play selected station.
-- K3 stop radio.
-- E2 select station.

local port = 5000
local ip = "192.168.0.22"
local dest = {ip, port}
local number = 0
local station = "Canut"


function init()
  station_name()
  norns.encoders.set_sens(2, 16)
end


function redraw()
  screen.clear()
  screen.move(1, 12)
  screen.text("OSC RADIO.")
  screen.move(24, 42)
  screen.text("Station : ")
  screen.font_face(5)
  screen.font_size(12)
  screen.text(station)
  screen.font_face(0)
  screen.font_size(8)
  screen.update()
end


function station_name()
  if number == 0 then
    station = "Canut"
  elseif number == 1 then
    station = "Fr. Musique"
  elseif number == 2 then
    station = "Fr. Info"
  elseif number == 3 then
    station = "Fr. Inter"
  elseif number == 4 then
    station = "Fr. Culture"
  elseif number == 5 then
    station = "FIP"
  elseif number < 0 then
    number = 0
  elseif number > 5 then
    number = 5
  end
end


function key(n, z)
  if n == 2 and z == 1 then
    osc.send(dest, "/play", {number})
  elseif n == 3 and z == 1 then
    osc.send(dest, "/stop", {1})
  elseif n == 1 then
    if n == 3 and z == 1 then
  end
    osc.send(dest, "/off", {1})
  end
end


function enc(n, d)
  if n == 2 then
    number = number + d
    station_name()
  end
  redraw()
end

