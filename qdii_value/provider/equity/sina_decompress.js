function sina_decompress (t) {
    var e, n, r, i, a, o, s, u = (arguments, 864e5), l = 7657, d = [], c = [], h = ~(3 << 30), f = 1 << 30, p = [0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30], m = Math, g = function () {
        var u, l;
        for (u = 0; 64 > u; u++)
            c[u] = m.pow(2, u),
                26 > u && (d[u] = v(u + 65),
                    d[u + 26] = v(u + 97),
                    10 > u && (d[u + 52] = v(u + 48)));
        for (d.push("+", "/"),
            d = d.join(""),
            n = t.split(""),
            r = n.length,
            u = 0; r > u; u++)
            n[u] = d.indexOf(n[u]);
        return i = {},
            e = o = 0,
            a = {},
            l = w([12, 6]),
            s = 63 ^ l[1],
            {
                _1479: P,
                _136: T,
                _200: k,
                _139: D,
                _197: _mi_run,
                _3466: _k2_run
            }["_" + l[0]] || function () {
                return []
            }
    }, v = String.fromCharCode, b = function (t) {
        return t === {}._
    }, y = function () {
        var t, e;
        for (t = N(),
            e = 1; ;) {
            if (!N())
                return e * (2 * t - 1);
            e++
        }
    }, N = function () {
        var t;
        return e >= r ? 0 : (t = n[e] & 1 << o,
            o++,
            o >= 6 && (o -= 6,
                e++),
            !!t)
    }, w = function (t, i, a) {
        var s, u, l, d, h;
        for (u = [],
            l = 0,
            i || (i = []),
            a || (a = []),
            s = 0; s < t.length; s++)
            if (d = t[s],
                l = 0,
                d) {
                if (e >= r)
                    return u;
                if (t[s] <= 0)
                    l = 0;
                else if (t[s] <= 30) {
                    for (; h = 6 - o,
                        h = d > h ? h : d,
                        l |= (n[e] >> o & (1 << h) - 1) << t[s] - d,
                        o += h,
                        o >= 6 && (o -= 6,
                            e++),
                        d -= h,
                        !(0 >= d);)
                        ;
                    i[s] && l >= c[t[s] - 1] && (l -= c[t[s]])
                } else
                    l = w([30, t[s] - 30], [0, i[s]]),
                        a[s] || (l = l[0] + l[1] * c[30]);
                u[s] = l
            } else
                u[s] = 0;
        return u
    }, _ = function () {
        var t;
        return t = w([3])[0],
            1 == t ? (i.d = w([18], [1])[0],
                t = 0) : t || (t = w([6])[0]),
            t
    }, x = function (t) {
        var e, n, r;
        for (t > 1 && (e = 0),
            e = 0; t > e; e++)
            i.d++,
                r = i.d % 7,
                (3 == r || 4 == r) && (i.d += 5 - r);
        return n = new Date,
            n.setTime((l + i.d) * u),
            n
    }, S = function (t) {
        var e, n, r;
        for (r = i.wd || 62,
            e = 0; t > e; e++)
            do
                i.d++;
            while (!(r & 1 << (i.d % 7 + 10) % 7));
        return n = new Date,
            n.setTime((l + i.d) * u),
            n
    }, C = function (t) {
        var e, n, r;
        return t ? 0 > t ? (e = C(-t),
            [-e[0], -e[1]]) : (e = t % 3,
                n = (t - e) / 3,
                r = [n, n],
                e && r[e - 1]++,
                r) : [0, 0]
    }, A = function (t, e, n) {
        var r, i, a;
        for (i = "number" == typeof e ? C(e) : e,
            a = C(n),
            r = [a[0] - i[0], a[1] - i[1]],
            i = 1; r[0] < r[1];)
            i *= 5,
                r[1]--;
        for (; r[1] < r[0];)
            i *= 2,
                r[0]--;
        if (i > 1 && (t *= i),
            r = r[0],
            t = _decnum(t),
            0 > r) {
            for (; t.length + r <= 0;)
                t = "0" + t;
            return r += t.length,
                i = t.substr(0, r) - 0,
                void 0 === n ? i + "." + t.substr(r) - 0 : (a = t.charAt(r) - 0,
                    a > 5 ? i++ : 5 == a && (t.substr(r + 1) - 0 > 0 ? i++ : i += 1 & i),
                    i)
        }
        for (; r > 0; r--)
            t += "0";
        return t - 0
    }, k = function () {
        var t, n, a, o, u;
        if (s >= 1)
            return [];
        for (i.d = w([18], [1])[0] - 1,
            a = w([3, 3, 30, 6]),
            i.p = a[0],
            i.ld = a[1],
            i.cd = a[2],
            i.c = a[3],
            i.m = m.pow(10, i.p),
            i.pc = i.cd / i.m,
            n = [],
            t = 0; o = {
                d: 1
            },
            N() && (a = w([3])[0],
                0 == a ? o.d = w([6])[0] : 1 == a ? (i.d = w([18])[0],
                    o.d = 0) : o.d = a),
            u = {
                date: x(o.d)
            },
            N() && (i.ld += y()),
            a = w([3 * i.ld], [1]),
            i.cd += a[0],
            u.close = i.cd / i.m,
            n.push(u),
            !(e >= r) && (e != r - 1 || 63 & (i.c ^ t + 1)); t++)
            ;
        return n[0].prevclose = i.pc, n
    }, T = function () {
        var t, n, a, o, u, l, d, c, h, f, p;
        if (s > 2)
            return [];
        for (d = [],
            h = {
                v: "volume",
                p: "price",
                a: "avg_price"
            },
            i.d = w([18], [1])[0] - 1,
            c = {
                date: x(1)
            },
            a = w(1 > s ? [3, 3, 4, 1, 1, 1, 5] : [4, 4, 4, 1, 1, 1, 3]),
            t = 0; 7 > t; t++)
            i[["la", "lp", "lv", "tv", "rv", "zv", "pp"][t]] = a[t];
        for (i.m = m.pow(10, i.pp),
            s >= 1 ? (a = w([3, 3]),
                i.c = a[0],
                a = a[1]) : (a = 5,
                    i.c = 2),
            i.pc = w([6 * a])[0],
            c.pc = i.pc / i.m,
            i.cp = i.pc,
            i.da = 0,
            i.sa = i.sv = 0,
            t = 0; !(e >= r) && (e != r - 1 || 7 & (i.c ^ t)); t++) {
            for (u = {},
                o = {},
                f = i.tv ? N() : 1,
                n = 0; 3 > n; n++)
                if (p = ["v", "p", "a"][n],
                    (f ? N() : 0) && (a = y(),
                        i["l" + p] += a),
                    l = "v" == p && i.rv ? N() : 1,
                    a = w([3 * i["l" + p] + ("v" == p ? 7 * l : 0)], [!!n])[0] * (l ? 1 : 100),
                    o[p] = a,
                    "v" == p) {
                    if (!(u[h[p]] = a) && (s > 1 || 241 > t) && (i.zv ? !N() : 1)) {
                        o.p = 0;
                        break
                    }
                } else
                    "a" == p && (i.da = (1 > s ? 0 : i.da) + o.a);
            i.sv += o.v,
                u[h.p] = (i.cp += o.p) / i.m,
                i.sa += o.v * i.cp,
                u[h.a] = b(o.a) ? t ? d[t - 1][h.a] : u[h.p] : i.sv ? ((m.floor((i.sa * (2e3 / i.m) + i.sv) / i.sv) >> 1) + i.da) / 1e3 : u[h.p] + i.da / 1e3,
                d.push(u)
        }
        return d[0].date = c.date,
            d[0].prevclose = c.pc,
            d
    }, P = function () {
        var t, e, n, r, a, o, u;
        if (s >= 1)
            return [];
        for (i.lv = 0,
            i.ld = 0,
            i.cd = 0,
            i.cv = [0, 0],
            i.p = w([6])[0],
            i.d = w([18], [1])[0] - 1,
            i.m = m.pow(10, i.p),
            a = w([3, 3]),
            i.md = a[0],
            i.mv = a[1],
            t = []; a = w([6]),
            a.length;) {
            if (n = {
                c: a[0]
            },
                r = {},
                n.d = 1,
                32 & n.c)
                for (; ;) {
                    if (a = w([6])[0],
                        63 == (16 | a)) {
                        u = 16 & a ? "x" : "u",
                            a = w([3, 3]),
                            n[u + "_d"] = a[0] + i.md,
                            n[u + "_v"] = a[1] + i.mv;
                        break
                    }
                    if (32 & a) {
                        o = 8 & a ? "d" : "v",
                            u = 16 & a ? "x" : "u",
                            n[u + "_" + o] = (7 & a) + i["m" + o];
                        break
                    }
                    if (o = 15 & a,
                        0 == o ? n.d = w([6])[0] : 1 == o ? (i.d = o = w([18])[0],
                            n.d = 0) : n.d = o,
                        !(16 & a))
                        break
                }
            r.date = x(n.d).toISOString().split('T')[0];  // modify;
            for (o in {
                v: 0,
                d: 0
            })
                b(n["x_" + o]) || (i["l" + o] = n["x_" + o]),
                    b(n["u_" + o]) && (n["u_" + o] = i["l" + o]);
            for (n.l_l = [n.u_d, n.u_d, n.u_d, n.u_d, n.u_v],
                u = p[15 & n.c],
                1 & n.u_v && (u = 31 - u),
                16 & n.c && (n.l_l[4] += 2),
                e = 0; 5 > e; e++)
                u & 1 << 4 - e && n.l_l[e]++,
                    n.l_l[e] *= 3;
            n.d_v = w(n.l_l, [1, 0, 0, 1, 1], [0, 0, 0, 0, 1]),
                o = i.cd + n.d_v[0],
                r.open = o / i.m,
                r.high = (o + n.d_v[1]) / i.m,
                r.low = (o - n.d_v[2]) / i.m,
                r.close = (o + n.d_v[3]) / i.m,
                a = n.d_v[4],
                "number" == typeof a && (a = [a, a >= 0 ? 0 : -1]),
                i.cd = o + n.d_v[3],
                u = i.cv[0] + a[0],
                i.cv = [u & h, i.cv[1] + a[1] + !!((i.cv[0] & h) + (a[0] & h) & f)],
                r.volume = (i.cv[0] & f - 1) + i.cv[1] * f,
                t.push(r)
        }
        return t
    }, D = function () {
        var t, e, n, r;
        if (s > 1)
            return [];
        for (i.l = 0,
            r = -1,
            i.d = w([18])[0] - 1,
            n = w([18])[0]; i.d < n;)
            e = x(1),
                0 >= r ? (N() && (i.l += y()),
                    r = w([3 * i.l], [0])[0] + 1,
                    t || (t = [e],
                        r--)) : t.push(e),
                r--;
        return t
    };
    return _mi_run = function () {
        var t, n, a, o;
        if (s >= 1)
            return [];
        for (i.f = w([6])[0],
            i.c = w([6])[0],
            a = [],
            i.dv = [],
            i.dl = [],
            t = 0; t < i.f; t++)
            i.dv[t] = 0,
                i.dl[t] = 0;
        for (t = 0; !(e >= r) && (e != r - 1 || 7 & (i.c ^ t)); t++) {
            for (o = [],
                n = 0; n < i.f; n++)
                N() && (i.dl[n] += y()),
                    i.dv[n] += w([3 * i.dl[n]], [1])[0],
                    o[n] = i.dv[n];
            a.push(o)
        }
        return a
    }
        ,
        _k2_run = function () {
            if (i = {
                b_avp: 1,
                b_ph: 0,
                b_phx: 0,
                b_sep: 0,
                p_p: 6,
                p_v: 0,
                p_a: 0,
                p_e: 0,
                p_t: 0,
                l_o: 3,
                l_h: 3,
                l_l: 3,
                l_c: 3,
                l_v: 5,
                l_a: 5,
                l_e: 3,
                l_t: 0,
                u_p: 0,
                u_v: 0,
                u_a: 0,
                wd: 62,
                d: 0
            },
                s > 0)
                return [];
            var t, n, a, o, u, l, d;
            for (t = []; ;) {
                if (e >= r)
                    return void 0;
                if (a = {
                    d: 1,
                    c: 0
                },
                    N())
                    if (N()) {
                        if (N()) {
                            for (a.c++,
                                a.a = i.b_avp,
                                N() && (i.b_avp ^= N(),
                                    i.b_ph ^= N(),
                                    i.b_phx ^= N(),
                                    a.s = i.b_sep,
                                    i.b_sep ^= N(),
                                    N() && (i.wd = w([7])[0]),
                                    a.s ^ i.b_sep && (a.s ? i.u_p = i.u_c : i.u_o = i.u_h = i.u_l = i.u_c = i.u_p)),
                                l = 0; l < 3 + 2 * i.b_ph; l++)
                                if (N() && (u = "pvaet".charAt(l),
                                    o = i["p_" + u],
                                    i["p_" + u] += y(),
                                    i["u_" + u] = A(i["u_" + u], o, i["p_" + u]) - 0,
                                    i.b_sep && !l))
                                    for (d = 0; 4 > d; d++)
                                        u = "ohlc".charAt(d),
                                            i["u_" + u] = A(i["u_" + u], o, i.p_p) - 0;
                            !i.b_avp && a.a && (i.u_a = A(n && n.amount || 0, 0, i.p_a))
                        }
                        if (N())
                            for (a.c++,
                                l = 0; l < 7 + i.b_ph + i.b_phx; l++)
                                N() && (6 == l ? a.d = _() : i["l_" + "ohlcva*et".charAt(l)] += y());
                        if (N() && (a.c++,
                            u = i.l_o + (N() && y()),
                            o = w([3 * u], [1])[0],
                            a.p = i.b_sep ? i.u_c + o : i.u_p += o),
                            !a.c)
                            break
                    } else
                        N() ? N() ? N() ? a.d = _() : i.l_v += y() : i.b_ph && N() ? i["l_" + "et".charAt(i.b_phx && N())] += y() : i.l_a += y() : i["l_" + "ohlc".charAt(w([2])[0])] += y();
                for (l = 0; l < 6 + i.b_ph + i.b_phx; l++)
                    d = "ohlcvaet".charAt(l),
                        o = (i.b_sep ? 191 : 185) >> l & 1,
                        a["v_" + d] = w([3 * i["l_" + d]], [o])[0];
                n = {
                    date: S(a.d).getTime()
                },
                    a.p && (n.prevclose = A(a.p, i.p_p)),
                    i.b_sep ? (n.open = A(i.u_o += a.v_o, i.p_p),
                        n.high = A(i.u_h += a.v_h, i.p_p),
                        n.low = A(i.u_l += a.v_l, i.p_p),
                        n.close = A(i.u_c += a.v_c, i.p_p)) : (a.o = i.u_p + a.v_o,
                            n.open = A(a.o, i.p_p),
                            n.high = A(a.o + a.v_h, i.p_p),
                            n.low = A(a.o - a.v_l, i.p_p),
                            n.close = A(i.u_p = a.o + a.v_c, i.p_p)),
                    n.volume = A(i.u_v += a.v_v, i.p_v),
                    i.b_avp ? (o = C(i.p_p),
                        u = C(i.p_v),
                        n.amount = A(A(Math.floor((i.b_sep ? (i.u_o + i.u_h + i.u_l + i.u_c) / 4 : a.o + (a.v_h - a.v_l + a.v_c) / 4) * i.u_v + .5), [o[0] + u[0], o[1] + u[1]], i.p_a) + a.v_a, i.p_a)) : (i.u_a += a.v_a,
                            n.amount = A(i.u_a, i.p_a)),
                    i.b_ph && (n.postVol = A(a.v_e, i.p_e),
                        n.postAmt = A(Math.floor(n.postVol * n.close + (i.b_phx ? A(a.v_t, i.p_t) : 0) + .5), 0)),
                    t.push(n)
            }
            return t
        }
        ,
        _decnum = function (t) {
            var e, n, r;
            if (t = (t || 0).toString(),
                r = [],
                n = t.toLowerCase().indexOf("e"),
                n > 0) {
                for (e = t.substr(n + 1) - 0; e >= 0; e--)
                    r.push(Math.floor(e * Math.pow(10, -e) + .5) - 0);
                return r.join("")
            }
            return t
        }
        ,
        g()()
}

((compressed) => JSON.stringify(sina_decompress(compressed)))