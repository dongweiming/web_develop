# coding=utf-8
import cPickle

import redis

r = redis.StrictRedis(host='localhost', port=6379)

review_ids = ['1471264', '1459361', '1464189']
r.set('review_ids', cPickle.dumps(review_ids))

promo_ids = [['2316772', ['2763629', '2762672', '2762640', '2762630', '2754153']],
             ['2278395', ['2768378', '2760752', '2775397', '2772461', '2773312']]]
r.set('promo_ids', cPickle.dumps(promo_ids))

boards = [[2422872, '无印良品风 静音棉拖'],
          [2741220, '斐讯FIR302E智能无线路由器'],
          [2769920, '安佳（Anchor）超高温灭菌全脂牛奶']]
r.set('boards', cPickle.dumps(boards))
r.set('promo_title', cPickle.dumps('本时段热门商品TOP3'))
r.set('promo_subtitle', cPickle.dumps('17：00 - 19：00'))
