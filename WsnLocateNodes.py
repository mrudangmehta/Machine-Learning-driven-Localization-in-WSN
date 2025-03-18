# WsnLocateNodes.py
# ***********************************************
# *   A New Algorithm to Locate WSN Nodes       *
# *                  by                         *
# *	         Mrudang Mehta                      *
# *	         Himanshu Mazumdar                  *
# *	      Date Start:- 20-August-2023           *
# *	     Update Date:- 20-August-2023           *
# ***********************************************

import math
import random
import sys
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import keyboard
import random
import os
import time
import threading
import threading as th
from random import randint

# ***********************************************
bm_main_width = 800  # canvas width
bm_main_height = 600  # canvas height
txbx_trx_rang = 33  # % of diagonal distance


# ***********************************************
class NODES:
    # pos = []
    nbrIds = []
    nbrDist = []


# ***********************************************
class NODRND:
    # pos = []
    nbrDist = []


# ***********************************************
def create_original_nodes(mx_nods):
    global nods_org, ri, noise
    nods_org = [NODES() for _ in range(mx_nods)]
    zoneX, zoneY = 6, 4
    sum1 = 0
    n1 = 0
    nn = 0
    nn_old = 0
    grp_sz = [0] * (zoneX * zoneY)
    nods_grp = mx_nods / (zoneX * zoneY)  # number of zones
    for y in range(zoneY):
        for x in range(zoneX):
            sum1 += nods_grp
            nn = int(sum1 + 0.5)
            grp_sz[n1] = nn - nn_old
            n1 += 1
            nn_old = nn

    offset = 0.025
    shrink = 1 - 2 * offset
    grp_w = (bm_main_width * shrink) / zoneX
    grp_h = (bm_main_height * shrink) / zoneY
    n1 = 0
    n2 = random.randint(0, zoneX * zoneY - 1)  # location of base stn.
    xn = n2 % zoneX
    yn = n2 // zoneX
    xb = xn * grp_w + random.random() * grp_w
    yb = yn * grp_h + random.random() * grp_h
    n = 0
    sum = 0
    h = 0
    sno = 0
    al2 = []
    offset = 0.025
    xo = bm_main_width * offset
    yo = bm_main_height * offset
    grp_org = [None] * (zoneX * zoneY)
    for y in range(zoneY):
        w = 0
        for x in range(zoneX):
            sum += nods_grp
            n += 1
            # if sno != n2:
            sum -= int(sum) % n
            grp_org[n - 1] = (w, h)
            w += grp_w
            for _ in range(grp_sz[n - 1]):
                xp = grp_org[n - 1][0] + random.random() * grp_w
                yp = grp_org[n - 1][1] + random.random() * grp_h
                nods_org[sno].pos = (xp + xo, yp + yo)
                xi = int(xp)
                yi = int(yp)
                al2.append(f"{str(xi).rjust(4, '0')},{str(yi).rjust(4, '0')},{sno}")
                sno += 1
        h += grp_h
    al2.sort()
    for i in range(len(al2)):
        nods_org[int(al2[i].split(",")[2])].id = i

    w = bm_main_width
    h = bm_main_height
    dmx = int(math.sqrt(w * w + h * h))
    ri = int(text_range.get("1.0", "end-1c"))
    rng = dmx * ri / 100
    ids = [0] * len(nods_org)
    for i in range(len(nods_org)):
        ids[nods_org[i].id] = i
    for i in range(len(nods_org)):
        ni = nods_org[i].id
        alno = []
        for j in range(len(nods_org)):
            nj = nods_org[j].id
            if ni != nj:
                dst = int(distance(nods_org[ni], nods_org[nj]))
                if dst <= rng:
                    alno.append(f"{str(dst).rjust(5, '0')},{nj}")
        alno.sort()
        id = ni
        # id = ids[i]
        nods_org[i].nbrIds = [0] * len(alno)
        nods_org[i].nbrDist = [0.0] * len(alno)
        nni = nods_org[i].id
        noise = float(text_nois.get("1.0", "end-1c"))
        err = noise / 100.0
        r1 = 1 - err
        r2 = 1 + err
        for j in range(len(alno)):
            w2 = alno[j].split(",")
            noise_now = random.uniform(r1, r2)
            nods_org[i].nbrDist[j] = float(w2[0]) * noise_now
            nods_org[i].nbrIds[j] = int(w2[1])
        a = 123
    a = 123


# ***********************************************
def distance(nd1, nd2):
    dst = math.sqrt((nd1.pos[0] - nd2.pos[0]) ** 2 + (nd1.pos[1] - nd2.pos[1]) ** 2)
    return dst


# ***********************************************
def mark_3_coordinates(nodes):
    area_mn = bm_main_width * bm_main_height / 100.0
    loop = 0
    while True:
        rn1 = random.randint(0, len(nodes) - 1)
        if len(nodes[rn1].nbrIds) >= 2:
            rn2 = random.randint(0, len(nodes[rn1].nbrIds) - 1)
            rn3 = random.randint(0, len(nodes[rn1].nbrIds) - 1)
            x1, y1 = nodes[rn1].pos
            x2, y2 = nodes[rn2].pos
            x3, y3 = nodes[rn3].pos
            a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
            b = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
            c = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            s = (a + b + c) / 2
            area = math.sqrt(s * (s - a) * (s - b) * (s - c))
            if area > area_mn:
                rns = [rn1, rn2, rn3]
                return rns
        loop += 1
        if loop > 10000:
            messagebox.showinfo("Selection Error", "Try New Nodes")
            break
    return None


# ***********************************************
def reset_sequence():
    global nod_rnd
    nod_rnd = []

    for i in range(len(nods_org)):
        new_node = NODRND()
        new_node.nbrDist = []
        new_node.id = nods_org[i].id
        new_node.pos = (0, 0)
        nod_rnd.append(new_node)
    

# ***********************************************
def randomize_sequence(pts3):
    global nod_rnd, ndx_dist
    w = bm_main_width * 1
    h = bm_main_height * 1
    nod_rnd = []

    for i in range(len(nods_org)):
        new_node = NODRND()
        new_node.nbrDist = []
        new_node.id = nods_org[i].id
        new_node.pos = (10 + random.randint(0, w - 20), 10 + random.randint(0, h - 20))
        nod_rnd.append(new_node)

    # plot_pts(nod_rnd)

    ndx_dist = []
    for i in range(len(nod_rnd)):
        row = []
        x1, y1 = nod_rnd[i].pos
        for j in range(len(nod_rnd)):
            x2, y2 = nod_rnd[j].pos
            dst = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            row.append(dst)
        ndx_dist.append(row)
        nod_rnd[i].nbrDist.append(row)
    nod_rnd[pts3[0]].pos = nods_org[pts3[0]].pos
    nod_rnd[pts3[1]].pos = nods_org[pts3[1]].pos
    nod_rnd[pts3[2]].pos = nods_org[pts3[2]].pos

    nds3 = None
    # rtbx_score.delete("1.0", "end")
    # eta = float(txbx_eta.get())


# ***********************************************
def btn_train_3_click():
    global eta, nds3, nod_rnd
    # eta = 0.00001
    eta = float(text_eta.get("1.0", "end-1c"))
    nds3 = mark_3_coordinates(nods_org)
    nod_rnd[nds3[0]].pos = nods_org[nds3[0]].pos
    nod_rnd[nds3[1]].pos = nods_org[nds3[1]].pos
    nod_rnd[nds3[2]].pos = nods_org[nds3[2]].pos
    # plot_pts(nod_rnd)
    tmr = th.Timer(0.01, timer2_tick)
    tmr.start()


# ***********************************************
def timer2_tick():
    global pts3, nod_rnd, loop, runcmd, errnow, btn_debug
    en = [0] * len(nods_org)
    if pts3 is None:
        pts3 = mark_3_coordinates(nods_org)
        nod_rnd[pts3[0]].pos = nods_org[pts3[0]].pos
        nod_rnd[pts3[1]].pos = nods_org[pts3[1]].pos
        nod_rnd[pts3[2]].pos = nods_org[pts3[2]].pos
    en[pts3[0]] = 1
    en[pts3[1]] = 1
    en[pts3[2]] = 1
    # test = [0.0 for _ in range(len(nods_org))]
    eta = float(text_eta.get("1.0", "end-1c"))
    for n in range(100):
        for i in range(len(nods_org)):
            sn = nods_org[i].id
            for j in range(len(nods_org[i].nbrIds)):
                dn = nods_org[i].nbrIds[j]
                dst_a = nods_org[i].nbrDist[j]
                dst_v = distance_v(nod_rnd[sn].pos, nod_rnd[dn].pos)
                av_err = dst_a - dst_v
                dX = nod_rnd[sn].pos[0] - nod_rnd[dn].pos[0]
                dY = nod_rnd[sn].pos[1] - nod_rnd[dn].pos[1]
                if en[sn] == 0:
                    nod_rnd[sn].pos = (
                        nod_rnd[sn].pos[0] + eta * dX * av_err,
                        nod_rnd[sn].pos[1] + eta * dY * av_err,
                    )
                if en[dn] == 0:
                    nod_rnd[dn].pos = (
                        nod_rnd[dn].pos[0] - eta * dX * av_err,
                        nod_rnd[dn].pos[1] - eta * dY * av_err,
                    )
    err, imx = calculate_position_error()
    loop += 1
    if loop >= 5:
        if round(err, 2) >= round(errnow, 2):
            if random.randint(0, 10) == 0:
                if noise <= 0:
                    randomize_sequence(pts3)
                else:
                    btn_debug.focus_set()
                    runcmd = False
            else:
                w = bm_main_width * 1
                h = bm_main_height * 1
                nod_rnd[imx].pos = (
                    10 + random.randint(0, w - 20),
                    10 + random.randint(0, h - 20),
                )
        loop = 0
    errnow = err
    draw_nodes(1)
    if errnow < 1.0:
        runcmd = False
    if runcmd == True:
        tmr = th.Timer(0.01, timer2_tick)
        tmr.start()
    else:
        if quitcmd == True:
            window.quit()


# ***********************************************
def calculate_position_error():
    global text_err
    errsum = 0
    errmx = 0
    imx = -1
    for i in range(len(nods_org)):
        ni = nod_rnd[i].id
        errx = abs(nods_org[i].pos[0] - nod_rnd[i].pos[0])
        erry = abs(nods_org[i].pos[1] - nod_rnd[i].pos[1])
        err = math.sqrt(errx * errx + erry * erry)
        if errmx < err:
            errmx = err
            imx = i
        errsum += err
    error = round(errsum / len(nods_org), 3)
    er = str(error)
    text_err.delete(1.0, "end")
    text_err.insert(tk.END, er)
    return error, imx


# ***********************************************
def distance_v(pt1, pt2):
    dst = math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    return dst


# # Draw node[] with sno ************************
def draw_nodes(locnods):
    global nodemx, screen_width, screen_height, distmax, txrange, distmax, nodeerr
    global gridX, gridY, ofsX, ofsY
    nodeerr = []
    mxnodes = int(nodemx)
    canvas.delete("all")
    nods = mxnodes
    draw_grid()
    for i in range(len(nods_org)):
        draw_this_node(i, "blue", 3, "white")
        nodeerr.append(0)
        if locnods == 1:
            draw_more_node(i)
            p1 = nods_org[pts3[0]].pos
            p2 = nods_org[pts3[1]].pos
            p3 = nods_org[pts3[2]].pos
            canvas.create_line(p1, p2, width=3, fill="#CC0000")
            canvas.create_line(p1, p3, width=3, fill="#CC0000")
            canvas.create_line(p2, p3, width=3, fill="#CC0000")
            None
    canvas.pack()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    a = 123


# Draw Grid ***************************************************
def draw_grid():
    global nodemx, screen_width, screen_height, gridX, gridY, ofsX, ofsY
    gridX, gridY = 6, 4
    gapx = (screen_width - 0) / gridX
    gapy = (screen_height - 0) / gridY
    for x in range(gridX + 1):
        xl = x * gapx
        canvas.create_line(
            xl, 0, xl, screen_height - 1, width=1, fill="#CCCCCC"
        )  # draw line
    for y in range(gridY + 1):
        yl = y * gapy
        canvas.create_line(
            0, yl, screen_width - 1, yl, width=1, fill="#CCCCCC"
        )  # draw line


# Draw One Node node[ndx] of width wdt ************************
def draw_this_node(ndx, col, wdt, bcol):
    global nods_org
    n20=30
    r = True
    ni = nods_org[ndx].id
    canvas.create_oval(
        nods_org[ni].pos[0],
        nods_org[ni].pos[1],
        nods_org[ni].pos[0] + n20,
        nods_org[ni].pos[1] + n20,
        fill=bcol,
        width=wdt,
        outline=col,
    )
    canvas.create_text(
        nods_org[ni].pos[0] + n20/2,
        nods_org[ni].pos[1] + n20/2,
        text=str(ni),
        # text=str(ndx),
        fill="black",
        font=("Helvetica 20 bold"),
    )
    return r


# ***********************************************
def draw_more_node(ndx):
    global nods_org
    r = True
    ni = nod_rnd[ndx].id
    canvas.create_text(
        nod_rnd[ni].pos[0] + 32,
        nod_rnd[ni].pos[1] + 32,
        text=str(ni),
        # text=str(ndx),
        fill="red",
        font=("Helvetica 20 bold"),
    )
    # p1 = nods_org[pts3[0]].pos
    # p2 = nods_org[pts3[1]].pos
    # p3 = nods_org[pts3[2]].pos
    # canvas.create_line(p1, p2, width=1, fill="#CC0000")
    # canvas.create_line(p1, p3, width=1, fill="#CC0000")
    # canvas.create_line(p2, p3, width=1, fill="#CC0000")
    return r


# ***********************************************
def btn_new_nodes():
    global pts3, nodemx
    nodemx = int(text_nodmx.get("1.0", "end-1c"))
    create_original_nodes(nodemx)
    # pts3 = mark_3_coordinates(nods_org)
    # randomize_sequence(pts3)
    draw_nodes(0)
    btn_ref3.focus_set()


# ***********************************************
def btn_redraw():
    global runcmd, btn_rand_nodes
    runcmd = False
    draw_nodes(0)
    btn_rand_nodes.focus_set()


# ***********************************************
def btn_references():
    a = 123
    global pts3, btn_rand_nodes
    pts3 = mark_3_coordinates(nods_org)
    reset_sequence()
    draw_nodes(1)
    btn_rand_nodes.focus_set()
    b = 123

# ***********************************************
def btn_randomize():
    global pts3, btn_rand_nodes
    # pts3 = mark_3_coordinates(nods_org)
    randomize_sequence(pts3)
    draw_nodes(1)
    btn_Localize.focus_set()


# ***********************************************
def btn_localize():
    global runcmd
    runcmd = True
    btn_train_3_click()
    btn_redrw.focus_set()


# ***********************************************
def get_nearest_node(pos):
    dstmx = sys.maxsize
    imx = 0
    for i in range(len(nod_rnd)):
        x = nod_rnd[i].pos[0]
        y = nod_rnd[i].pos[1]
        dst2 = (x - pos[0]) ** 2 + (y - pos[1]) ** 2
        if dstmx > dst2:
            dstmx = dst2
            imx = i
    return imx
    None


# ***********************************************
def update_nod_rnd_position(nodno, posd):
    global nod_rnd
    nod_rnd[nodno].pos = (
        nod_rnd[nodno].pos[0] + posd[0],
        nod_rnd[nodno].pos[1] + posd[1],
    )
    ndx_dist = []
    for i in range(len(nod_rnd)):
        row = []
        x1, y1 = nod_rnd[i].pos
        for j in range(len(nod_rnd)):
            x2, y2 = nod_rnd[j].pos
            dst = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            row.append(dst)
        ndx_dist.append(row)
        nod_rnd[i].nbrDist.append(row)
    nod_rnd[pts3[0]].pos = nods_org[pts3[0]].pos
    nod_rnd[pts3[1]].pos = nods_org[pts3[1]].pos
    nod_rnd[pts3[2]].pos = nods_org[pts3[2]].pos
    draw_nodes(1)
    a = 123
    None


# ***********************************************
def on_mouse_press(event):
    global mouse_position
    mouse_position = (event.x, event.y)


# ***********************************************
def on_mouse_release(event):
    x, y = event.x, event.y
    nodno = get_nearest_node(mouse_position)
    posd = x - mouse_position[0], y - mouse_position[1]
    update_nod_rnd_position(nodno, posd)
    a = 123


# ***********************************************
def debug():
    global mxnodes, nodemx, runcmd
    runcmd = False
    return
    arr = []
    for i in range(1, 11):
        mx_nods = i * 10
        nodemx = mx_nods
        for j in range(1, 21):
            ri = j * 5
            text_range.delete("1.0", tk.END)
            text_range.insert(tk.END, str(ri))
            create_original_nodes(mx_nods)
            draw_nodes(0)

            avg = 0
            for i in range(len(nods_org)):
                # print(nods_org[i].id)
                # print(nods_org[i].nbrIds)
                # arr.append(nods_org[i].id)
                # arr.append(nods_org[i].nbrIds)
                avg += len(nods_org[i].nbrIds)
            avg = avg / len(nods_org)
            row = []
            row.append(" Nodes:" + str(len(nods_org)))
            row.append(" Range:" + str(ri))
            avg2 = "{:.2f}".format(avg)
            row.append(" Avg Nbrs:" + avg2)
            arr.append(row)
        arr.append("............................")

    display_array_in_notepad(arr)
    a = 123


# ***********************************************
def display_array_in_notepad(arr):
    array_string = "\n".join(map(str, arr))
    with open("DebugOut.txt", "w") as f:
        f.write(array_string)
    import os

    os.system("DebugOut.txt")


# ***********************************************
def quit_app():
    global runcmd, quitcmd
    if runcmd == False:
        window.quit()
    quitcmd = True
    runcmd = False


# ***********************************************
def main_menu():
    global window, canvas, text_nodmx, text_range, loop, btn_ref3
    global screen_width, screen_height, btn_redrw, text_err, text_nois
    global gridX, gridY, runcmd, btn_rand_nodes, btn_Localize, text_eta
    global btn_debug
    window = tk.Tk()
    window.title("WSN Localizing: Machine Learning")
    screen_width, screen_height = 800, 700
    ofsX, ofsY = 0, 0
    canvas = tk.Canvas(window, width=screen_width, height=screen_height, bg="white")
    canvas.pack(side="left")
    place1 = tk.Frame(window, bg="LightGray")
    place1.pack(side="right", padx=10, pady=10, fill="y")
    lblin = tk.Label(place1, text="Max Nodes", fg="black", font='sans 16 bold')
    lblin.pack(padx=2, pady=4, fill="x")
    text_nodmx = tk.Text(place1, height=1, width=10, font='sans 16 bold')
    text_nodmx.pack(padx=2, pady=1)
    text_nodmx.insert(tk.END, "10")
    lblrng = tk.Label(place1, text="Trx Range %", fg="black", font='sans 16 bold')
    lblrng.pack(padx=2, pady=4, fill="x")
    text_range = tk.Text(place1, height=1, width=10, font='sans 16 bold')
    text_range.pack(padx=2, pady=1)
    text_range.insert(tk.END, "99")
    lbleta = tk.Label(place1, text="Lurning Rate", fg="black", font='sans 16 bold')
    lbleta.pack(padx=2, pady=4, fill="x")
    text_eta = tk.Text(place1, height=1, width=10, font='sans 16 bold')
    text_eta.pack(padx=2, pady=1)
    text_eta.insert(tk.END, "0.00002")

    lblnois = tk.Label(place1, text="RF Noise %", fg="black", font='sans 16 bold')
    lblnois.pack(padx=2, pady=4, fill="x")
    text_nois = tk.Text(place1, height=1, width=10, font='sans 16 bold')
    text_nois.pack(padx=2, pady=1)
    text_nois.insert(tk.END, "0.0")

    lblerr = tk.Label(place1, text="Localize Error", fg="black", font='sans 16 bold')
    lblerr.pack(padx=2, pady=4, fill="x")
    text_err = tk.Text(place1, height=1, width=10, font='sans 16 bold')
    text_err.pack(padx=2, pady=1)
    text_err.insert(tk.END, "0.0")

    btn_nodes = tk.Button(
        place1, text="New Nodes", bg="lightgray", command=btn_new_nodes, font='sans 16 bold'
    )
    btn_nodes.focus_set()
    btn_nodes.pack(padx=2, pady=4, anchor="ne", fill="x")
    btn_redrw = tk.Button(place1, text="Re Draw", bg="lightgray", command=btn_redraw, font='sans 16 bold')
    btn_redrw.pack(padx=2, pady=4, anchor="ne", fill="x")
    btn_ref3 = tk.Button(
        place1, text="3 Ref. Pts", bg="lightgray", command=btn_references, font='sans 16 bold'
    )
    btn_ref3.pack(padx=2, pady=4, anchor="ne", fill="x")
    btn_rand_nodes = tk.Button(
        place1, text="Randomize", bg="lightgray", command=btn_randomize, font='sans 16 bold'
    )
    btn_rand_nodes.pack(padx=2, pady=4, anchor="ne", fill="x")
    btn_Localize = tk.Button(
        place1, text="Localize", bg="lightgray", command=btn_localize, font='sans 16 bold'
    )
    btn_Localize.pack(padx=2, pady=4, anchor="ne", fill="x")

    btn_debug = tk.Button(place1, text="Pause", bg="lightgray", command=debug, font='sans 16 bold')
    btn_debug.pack(padx=2, pady=4, anchor="ne", fill="x")

    btn_exit = tk.Button(place1, text="Exit", bg="lightgray", command=quit_app, font='sans 16 bold')
    btn_exit.pack(anchor="sw", fill="x")

    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)
    loop = 0
    window.mainloop()


# Start the program *****************************
runcmd = False
quitcmd = False
main_menu()
# ***********************************************
