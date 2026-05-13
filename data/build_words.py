"""
构建KET词库JSON - 包含所有198词的KET标准例句
句长：6-12词；时态：一般现在/过去/将来时；词汇：KET考纲内
"""
import json

WORDS_DATA = [
  # ── 人物性格&能力 ──
  {"id":1,"word":"able","phonetic":"/ˈeɪbl/","part":"adj.","meaning":"有能力的，能够","topic":"人物性格&能力","level":"A",
   "s1":"I am **able** to swim very well.","s1c":"我很会游泳。",
   "s2":"She is **able** to finish her homework on time.","s2c":"她能按时完成作业。"},

  {"id":2,"word":"active","phonetic":"/ˈæktɪv/","part":"adj.","meaning":"积极的，活跃的","topic":"人物性格&能力","level":"A",
   "s1":"My little brother is very **active** at school.","s1c":"我弟弟在学校很活跃。",
   "s2":"She likes **active** sports like running and swimming.","s2c":"她喜欢跑步和游泳这样的运动。"},

  {"id":3,"word":"brave","phonetic":"/breɪv/","part":"adj.","meaning":"勇敢的","topic":"人物性格&能力","level":"A",
   "s1":"The boy was very **brave** at the dentist.","s1c":"那个男孩在牙医那里非常勇敢。",
   "s2":"You must be **brave** when you feel scared.","s2c":"当你感到害怕时，要勇敢。"},

  {"id":4,"word":"calm","phonetic":"/kɑːm/","part":"adj.","meaning":"冷静的","topic":"人物性格&能力","level":"A",
   "s1":"Please stay **calm** and listen to the teacher.","s1c":"请保持冷静，听老师说话。",
   "s2":"She is always **calm** before her exams.","s2c":"她考试前总是很冷静。"},

  {"id":5,"word":"careful","phonetic":"/ˈkeəfl/","part":"adj.","meaning":"小心的，仔细的","topic":"人物性格&能力","level":"A",
   "s1":"Be **careful** when you cross the road.","s1c":"过马路时要小心。",
   "s2":"She is very **careful** with her schoolwork.","s2c":"她对学业非常仔细认真。"},

  {"id":6,"word":"clever","phonetic":"/ˈklevə/","part":"adj.","meaning":"聪明的","topic":"人物性格&能力","level":"A",
   "s1":"My friend is very **clever** at maths.","s1c":"我的朋友数学很聪明。",
   "s2":"That was a **clever** answer to the question.","s2c":"那是对这道题非常聪明的回答。"},

  {"id":7,"word":"confident","phonetic":"/ˈkɒnfɪdənt/","part":"adj.","meaning":"自信的","topic":"人物性格&能力","level":"A",
   "s1":"She felt very **confident** before the show.","s1c":"演出前她感到非常自信。",
   "s2":"He is **confident** about his English test.","s2c":"他对英语考试很有信心。"},

  {"id":8,"word":"creative","phonetic":"/kriˈeɪtɪv/","part":"adj.","meaning":"有创造力的","topic":"人物性格&能力","level":"A",
   "s1":"My sister is very **creative** and loves painting.","s1c":"我姐姐很有创造力，喜欢画画。",
   "s2":"We need **creative** ideas for the school project.","s2c":"我们需要有创意的想法来做学校项目。"},

  {"id":9,"word":"friendly","phonetic":"/ˈfrendli/","part":"adj.","meaning":"友好的","topic":"人物性格&能力","level":"A",
   "s1":"The new teacher is very **friendly** to all students.","s1c":"新老师对所有学生都很友好。",
   "s2":"Everyone in my class is **friendly** and helpful.","s2c":"我班上的每个人都友好且乐于助人。"},

  {"id":10,"word":"generous","phonetic":"/ˈdʒenərəs/","part":"adj.","meaning":"大方的，慷慨的","topic":"人物性格&能力","level":"A",
   "s1":"My grandfather is very **generous** with his money.","s1c":"我爷爷花钱很大方。",
   "s2":"She is **generous** and always shares her food.","s2c":"她很慷慨，总是分享她的食物。"},

  {"id":11,"word":"honest","phonetic":"/ˈɒnɪst/","part":"adj.","meaning":"诚实的","topic":"人物性格&能力","level":"A",
   "s1":"It is important to be **honest** with your friends.","s1c":"对朋友诚实是很重要的。",
   "s2":"An **honest** person always tells the truth.","s2c":"诚实的人总是说实话。"},

  {"id":12,"word":"kind","phonetic":"/kaɪnd/","part":"adj.","meaning":"善良的","topic":"人物性格&能力","level":"A",
   "s1":"It was very **kind** of you to help me.","s1c":"你帮助我真是太好了。",
   "s2":"She is **kind** to animals and loves cats.","s2c":"她对动物很善良，喜欢猫。"},

  {"id":13,"word":"lazy","phonetic":"/ˈleɪzi/","part":"adj.","meaning":"懒惰的","topic":"人物性格&能力","level":"A",
   "s1":"Don't be **lazy** – finish your homework first.","s1c":"不要懒惰，先把作业做完。",
   "s2":"My cat is very **lazy** and sleeps all day.","s2c":"我的猫很懒，整天睡觉。"},

  {"id":14,"word":"patient","phonetic":"/ˈpeɪʃnt/","part":"adj.","meaning":"有耐心的","topic":"人物性格&能力","level":"A",
   "s1":"Good teachers are always **patient** with their students.","s1c":"好老师总是对学生很有耐心。",
   "s2":"You need to be **patient** when you learn a new skill.","s2c":"学习新技能时需要有耐心。"},

  {"id":15,"word":"polite","phonetic":"/pəˈlaɪt/","part":"adj.","meaning":"有礼貌的","topic":"人物性格&能力","level":"A",
   "s1":"It is **polite** to say thank you after a meal.","s1c":"饭后说谢谢是有礼貌的。",
   "s2":"She is always **polite** and says please and thank you.","s2c":"她总是很有礼貌，说请和谢谢。"},

  {"id":16,"word":"quiet","phonetic":"/ˈkwaɪət/","part":"adj.","meaning":"安静的","topic":"人物性格&能力","level":"A",
   "s1":"Please be **quiet** in the library.","s1c":"在图书馆请保持安静。",
   "s2":"She is a **quiet** girl but very clever.","s2c":"她是个安静的女孩，但很聪明。"},

  {"id":17,"word":"shy","phonetic":"/ʃaɪ/","part":"adj.","meaning":"害羞的","topic":"人物性格&能力","level":"A",
   "s1":"He is too **shy** to speak in front of the class.","s1c":"他太害羞了，不敢在全班面前讲话。",
   "s2":"She was **shy** on her first day at school.","s2c":"她第一天上学时很害羞。"},

  {"id":18,"word":"smart","phonetic":"/smɑːt/","part":"adj.","meaning":"机灵的，聪明的","topic":"人物性格&能力","level":"A",
   "s1":"That was a very **smart** idea!","s1c":"那是个非常聪明的主意！",
   "s2":"She is **smart** and always gets good marks.","s2c":"她很聪明，总是得高分。"},

  {"id":19,"word":"strict","phonetic":"/strɪkt/","part":"adj.","meaning":"严格的","topic":"人物性格&能力","level":"A",
   "s1":"Our maths teacher is very **strict** about homework.","s1c":"我们的数学老师对作业非常严格。",
   "s2":"My parents are **strict** but they care about me.","s2c":"我的父母很严格，但他们关心我。"},

  {"id":20,"word":"thoughtful","phonetic":"/ˈθɔːtfl/","part":"adj.","meaning":"体贴的","topic":"人物性格&能力","level":"A",
   "s1":"It was **thoughtful** of her to bring me a gift.","s1c":"她给我带礼物真是很体贴。",
   "s2":"He is a **thoughtful** son and always helps his mother.","s2c":"他是个体贴的儿子，总是帮助妈妈。"},

  # ── 校园学习&日常动作 ──
  {"id":21,"word":"attend","phonetic":"/əˈtend/","part":"v.","meaning":"参加，出席","topic":"校园学习&日常动作","level":"A",
   "s1":"All students must **attend** the morning meeting.","s1c":"所有学生必须参加早上的会议。",
   "s2":"Did you **attend** the school sports day last week?","s2c":"你上周参加学校运动日了吗？"},

  {"id":22,"word":"borrow","phonetic":"/ˈbɒrəʊ/","part":"v.","meaning":"借入，借","topic":"校园学习&日常动作","level":"A",
   "s1":"Can I **borrow** your pen, please?","s1c":"请问我能借你的笔吗？",
   "s2":"She **borrowed** a book from the school library.","s2c":"她从学校图书馆借了一本书。"},

  {"id":23,"word":"complete","phonetic":"/kəmˈpliːt/","part":"v.","meaning":"完成","topic":"校园学习&日常动作","level":"A",
   "s1":"Please **complete** your homework before dinner.","s1c":"请在晚饭前完成你的作业。",
   "s2":"He **completed** all the questions in the test.","s2c":"他完成了考试中的所有题目。"},

  {"id":24,"word":"copy","phonetic":"/ˈkɒpi/","part":"v.","meaning":"抄写，复制","topic":"校园学习&日常动作","level":"A",
   "s1":"Please **copy** the sentences into your notebook.","s1c":"请把句子抄写到你的笔记本上。",
   "s2":"Do not **copy** your friend's answers in the test.","s2c":"考试中不要抄你朋友的答案。"},

  {"id":25,"word":"discuss","phonetic":"/dɪˈskʌs/","part":"v.","meaning":"讨论","topic":"校园学习&日常动作","level":"A",
   "s1":"Let's **discuss** our plans for the school trip.","s1c":"我们来讨论一下学校旅行的计划。",
   "s2":"The class **discussed** the story for ten minutes.","s2c":"全班讨论了这个故事十分钟。"},

  {"id":26,"word":"explain","phonetic":"/ɪkˈspleɪn/","part":"v.","meaning":"解释","topic":"校园学习&日常动作","level":"A",
   "s1":"Can you **explain** the rule again, please?","s1c":"请你再解释一遍这个规则好吗？",
   "s2":"The teacher **explained** the new words clearly.","s2c":"老师清楚地解释了新单词。"},

  {"id":27,"word":"finish","phonetic":"/ˈfɪnɪʃ/","part":"v.","meaning":"结束，完成","topic":"校园学习&日常动作","level":"A",
   "s1":"I **finished** my homework before dinner.","s1c":"我在晚饭前完成了作业。",
   "s2":"Have you **finished** reading that book yet?","s2c":"你读完那本书了吗？"},

  {"id":28,"word":"forget","phonetic":"/fəˈɡet/","part":"v.","meaning":"忘记","topic":"校园学习&日常动作","level":"A",
   "s1":"Don't **forget** to bring your school bag tomorrow.","s1c":"别忘了明天带你的书包。",
   "s2":"She **forgot** her lunch at home this morning.","s2c":"今天早上她把午饭忘在家里了。"},

  {"id":29,"word":"join","phonetic":"/dʒɔɪn/","part":"v.","meaning":"加入","topic":"校园学习&日常动作","level":"A",
   "s1":"Would you like to **join** our reading club?","s1c":"你想加入我们的阅读俱乐部吗？",
   "s2":"He **joined** the school football team last year.","s2c":"他去年加入了学校足球队。"},

  {"id":30,"word":"learn","phonetic":"/lɜːn/","part":"v.","meaning":"学习","topic":"校园学习&日常动作","level":"A",
   "s1":"I am learning to **learn** new English words every day.","s1c":"我每天都在学新的英语单词。",
   "s2":"She **learnt** to ride a bike when she was six.","s2c":"她六岁时学会了骑自行车。"},

  {"id":31,"word":"lend","phonetic":"/lend/","part":"v.","meaning":"借出","topic":"校园学习&日常动作","level":"A",
   "s1":"Can you **lend** me your ruler for a minute?","s1c":"你能把你的尺借给我一下吗？",
   "s2":"She **lent** her dictionary to her classmate.","s2c":"她把词典借给了她的同学。"},

  {"id":32,"word":"miss","phonetic":"/mɪs/","part":"v.","meaning":"错过，想念","topic":"校园学习&日常动作","level":"A",
   "s1":"I **missed** the school bus this morning.","s1c":"今天早上我错过了校车。",
   "s2":"She **misses** her old friends from primary school.","s2c":"她很想念小学时的老朋友。"},

  {"id":33,"word":"practise","phonetic":"/ˈpræktɪs/","part":"v.","meaning":"练习","topic":"校园学习&日常动作","level":"A",
   "s1":"You should **practise** your English every day.","s1c":"你应该每天练习英语。",
   "s2":"She **practised** the piano for one hour after school.","s2c":"她放学后练了一个小时的钢琴。"},

  {"id":34,"word":"prepare","phonetic":"/prɪˈpeə/","part":"v.","meaning":"准备","topic":"校园学习&日常动作","level":"A",
   "s1":"I **prepared** my bag the night before school.","s1c":"我在上学前一晚准备好了书包。",
   "s2":"Let's **prepare** for the English test together.","s2c":"让我们一起为英语考试做准备。"},

  {"id":35,"word":"promise","phonetic":"/ˈprɒmɪs/","part":"v.","meaning":"承诺","topic":"校园学习&日常动作","level":"A",
   "s1":"I **promise** to finish my homework tonight.","s1c":"我答应今晚完成作业。",
   "s2":"She **promised** her mum to be home by five.","s2c":"她答应妈妈五点前回家。"},

  {"id":36,"word":"remember","phonetic":"/rɪˈmembə/","part":"v.","meaning":"记得","topic":"校园学习&日常动作","level":"A",
   "s1":"**Remember** to take your book to class.","s1c":"记得带你的书去上课。",
   "s2":"Do you **remember** the words from last week?","s2c":"你记得上周的单词吗？"},

  {"id":37,"word":"repeat","phonetic":"/rɪˈpiːt/","part":"v.","meaning":"重复","topic":"校园学习&日常动作","level":"A",
   "s1":"Please **repeat** the word after the teacher.","s1c":"请跟着老师重复这个单词。",
   "s2":"Can you **repeat** that sentence more slowly?","s2c":"你能把那个句子说得慢一点吗？"},

  {"id":38,"word":"share","phonetic":"/ʃeə/","part":"v.","meaning":"分享","topic":"校园学习&日常动作","level":"A",
   "s1":"Please **share** your ideas with the class.","s1c":"请和全班分享你的想法。",
   "s2":"She **shared** her lunch with her best friend.","s2c":"她和最好的朋友分享了午饭。"},

  {"id":39,"word":"study","phonetic":"/ˈstʌdi/","part":"v.","meaning":"学习，用功","topic":"校园学习&日常动作","level":"A",
   "s1":"I **study** English for two hours every evening.","s1c":"我每天晚上学习英语两个小时。",
   "s2":"She **studied** hard and passed all her exams.","s2c":"她努力学习，通过了所有考试。"},

  {"id":40,"word":"waste","phonetic":"/weɪst/","part":"v.","meaning":"浪费","topic":"校园学习&日常动作","level":"A",
   "s1":"Don't **waste** your time playing games all day.","s1c":"不要整天玩游戏浪费时间。",
   "s2":"It is bad to **waste** food and water.","s2c":"浪费食物和水是不好的。"},

  # ── 日常生活&饮食购物 ──
  {"id":41,"word":"afford","phonetic":"/əˈfɔːd/","part":"v.","meaning":"买得起","topic":"日常生活&饮食购物","level":"B",
   "s1":"We cannot **afford** to buy a new computer now.","s1c":"我们现在买不起新电脑。",
   "s2":"Can you **afford** the price of that jacket?","s2c":"你买得起那件夹克吗？"},

  {"id":42,"word":"bargain","phonetic":"/ˈbɑːɡɪn/","part":"n.","meaning":"便宜货","topic":"日常生活&饮食购物","level":"B",
   "s1":"This coat was a real **bargain** – only ten pounds!","s1c":"这件外套真是便宜货——只要十英镑！",
   "s2":"Mum loves to find a good **bargain** at the market.","s2c":"妈妈喜欢在市场上找便宜货。"},

  {"id":43,"word":"buy","phonetic":"/baɪ/","part":"v.","meaning":"购买","topic":"日常生活&饮食购物","level":"B",
   "s1":"I want to **buy** a new book this weekend.","s1c":"我这周末想买一本新书。",
   "s2":"She **bought** some fruit at the market yesterday.","s2c":"她昨天在市场买了一些水果。"},

  {"id":44,"word":"cheap","phonetic":"/tʃiːp/","part":"adj.","meaning":"便宜的","topic":"日常生活&饮食购物","level":"B",
   "s1":"These shoes are very **cheap** and comfortable.","s1c":"这些鞋子很便宜而且舒适。",
   "s2":"Is there a **cheap** restaurant near here?","s2c":"这附近有便宜的餐厅吗？"},

  {"id":45,"word":"choose","phonetic":"/tʃuːz/","part":"v.","meaning":"选择","topic":"日常生活&饮食购物","level":"B",
   "s1":"Please **choose** a book from the shelf.","s1c":"请从书架上选一本书。",
   "s2":"She **chose** the blue dress for the party.","s2c":"她为派对选了蓝色连衣裙。"},

  {"id":46,"word":"cost","phonetic":"/kɒst/","part":"v.","meaning":"花费","topic":"日常生活&饮食购物","level":"B",
   "s1":"This book **costs** ten pounds.","s1c":"这本书花了十英镑。",
   "s2":"How much does the ticket **cost**?","s2c":"这张票多少钱？"},

  {"id":47,"word":"delicious","phonetic":"/dɪˈlɪʃəs/","part":"adj.","meaning":"美味的","topic":"日常生活&饮食购物","level":"B",
   "s1":"This cake is really **delicious**!","s1c":"这个蛋糕真的太好吃了！",
   "s2":"Mum made a **delicious** soup for dinner.","s2c":"妈妈做了一道美味的汤作为晚餐。"},

  {"id":48,"word":"expensive","phonetic":"/ɪkˈspensɪv/","part":"adj.","meaning":"昂贵的","topic":"日常生活&饮食购物","level":"B",
   "s1":"That coat is too **expensive** for me.","s1c":"那件外套对我来说太贵了。",
   "s2":"Eating at that restaurant is very **expensive**.","s2c":"在那家餐厅吃饭非常贵。"},

  {"id":49,"word":"fresh","phonetic":"/freʃ/","part":"adj.","meaning":"新鲜的","topic":"日常生活&饮食购物","level":"B",
   "s1":"I like to eat **fresh** fruit every morning.","s1c":"我喜欢每天早上吃新鲜水果。",
   "s2":"The bread from the bakery is always **fresh**.","s2c":"面包店的面包总是新鲜的。"},

  {"id":50,"word":"hungry","phonetic":"/ˈhʌŋɡri/","part":"adj.","meaning":"饥饿的","topic":"日常生活&饮食购物","level":"B",
   "s1":"I am very **hungry** after school.","s1c":"放学后我非常饿。",
   "s2":"Are you **hungry**? Let's have a snack.","s2c":"你饿了吗？我们来吃点零食吧。"},

  {"id":51,"word":"menu","phonetic":"/ˈmenjuː/","part":"n.","meaning":"菜单","topic":"日常生活&饮食购物","level":"B",
   "s1":"Could we see the **menu**, please?","s1c":"请问我们可以看菜单吗？",
   "s2":"The **menu** at this café looks really good.","s2c":"这家咖啡馆的菜单看起来很不错。"},

  {"id":52,"word":"order","phonetic":"/ˈɔːdə/","part":"v.","meaning":"点餐，订购","topic":"日常生活&饮食购物","level":"B",
   "s1":"I would like to **order** a sandwich, please.","s1c":"我想点一个三明治，谢谢。",
   "s2":"She **ordered** a pizza and a glass of juice.","s2c":"她点了一份披萨和一杯果汁。"},

  {"id":53,"word":"price","phonetic":"/praɪs/","part":"n.","meaning":"价格","topic":"日常生活&饮食购物","level":"B",
   "s1":"What is the **price** of this T-shirt?","s1c":"这件T恤的价格是多少？",
   "s2":"The **price** of food is higher this year.","s2c":"今年食品的价格更高了。"},

  {"id":54,"word":"receive","phonetic":"/rɪˈsiːv/","part":"v.","meaning":"收到","topic":"日常生活&饮食购物","level":"B",
   "s1":"I **received** a lovely birthday card from my friend.","s1c":"我收到了朋友寄来的漂亮生日贺卡。",
   "s2":"She **received** a prize for her painting.","s2c":"她因为她的画作获得了一个奖。"},

  {"id":55,"word":"sell","phonetic":"/sel/","part":"v.","meaning":"售卖","topic":"日常生活&饮食购物","level":"B",
   "s1":"This shop **sells** books and magazines.","s1c":"这家店出售书籍和杂志。",
   "s2":"They **sold** all the cakes by lunchtime.","s2c":"他们在午饭前就把蛋糕全部卖完了。"},

  {"id":56,"word":"taste","phonetic":"/teɪst/","part":"v./n.","meaning":"品尝/味道","topic":"日常生活&饮食购物","level":"B",
   "s1":"This soup **tastes** very good.","s1c":"这道汤味道很好。",
   "s2":"**Taste** this apple – it is very sweet.","s2c":"尝一尝这个苹果——它非常甜。"},

  {"id":57,"word":"thirsty","phonetic":"/ˈθɜːsti/","part":"adj.","meaning":"口渴的","topic":"日常生活&饮食购物","level":"B",
   "s1":"I am very **thirsty** after running.","s1c":"跑步后我非常渴。",
   "s2":"Are you **thirsty**? Have some water.","s2c":"你渴了吗？喝点水吧。"},

  {"id":58,"word":"traditional","phonetic":"/trəˈdɪʃənl/","part":"adj.","meaning":"传统的","topic":"日常生活&饮食购物","level":"B",
   "s1":"We eat **traditional** food at New Year.","s1c":"我们在新年吃传统食物。",
   "s2":"She wore a **traditional** dress at the festival.","s2c":"她在节日上穿了一件传统服装。"},

  {"id":59,"word":"value","phonetic":"/ˈvæljuː/","part":"n.","meaning":"价值","topic":"日常生活&饮食购物","level":"B",
   "s1":"This bag is good **value** for money.","s1c":"这个包物有所值。",
   "s2":"Family is the most important **value** in life.","s2c":"家庭是生活中最重要的价值。"},

  # ── 出行旅游&环境天气 ──
  {"id":60,"word":"airport","phonetic":"/ˈeəpɔːt/","part":"n.","meaning":"机场","topic":"出行旅游&环境天气","level":"B",
   "s1":"We arrived at the **airport** two hours early.","s1c":"我们提前两小时到达了机场。",
   "s2":"The **airport** is far from the city centre.","s2c":"机场离市中心很远。"},

  {"id":61,"word":"arrive","phonetic":"/əˈraɪv/","part":"v.","meaning":"到达","topic":"出行旅游&环境天气","level":"B",
   "s1":"What time does the train **arrive** in London?","s1c":"火车几点到达伦敦？",
   "s2":"She **arrived** at school ten minutes late.","s2c":"她上学迟到了十分钟。"},

  {"id":62,"word":"bridge","phonetic":"/brɪdʒ/","part":"n.","meaning":"桥","topic":"出行旅游&环境天气","level":"B",
   "s1":"We walked across a long **bridge** over the river.","s1c":"我们走过了一座横跨河流的长桥。",
   "s2":"There is an old **bridge** near our village.","s2c":"我们村附近有一座古老的桥。"},

  {"id":63,"word":"countryside","phonetic":"/ˈkʌntrisaɪd/","part":"n.","meaning":"乡村","topic":"出行旅游&环境天气","level":"B",
   "s1":"I love walking in the **countryside** at weekends.","s1c":"我喜欢在周末去乡村散步。",
   "s2":"The **countryside** is quiet and very beautiful.","s2c":"乡村很安静，非常美丽。"},

  {"id":64,"word":"direction","phonetic":"/dɪˈrekʃn/","part":"n.","meaning":"方向","topic":"出行旅游&环境天气","level":"B",
   "s1":"Can you tell me the **direction** to the station?","s1c":"你能告诉我去车站的方向吗？",
   "s2":"We followed the **direction** on the map.","s2c":"我们按照地图上的方向走。"},

  {"id":65,"word":"forest","phonetic":"/ˈfɒrɪst/","part":"n.","meaning":"森林","topic":"出行旅游&环境天气","level":"B",
   "s1":"We saw many animals in the **forest**.","s1c":"我们在森林里看到了许多动物。",
   "s2":"The **forest** near our town is very old.","s2c":"我们镇附近的森林非常古老。"},

  {"id":66,"word":"journey","phonetic":"/ˈdʒɜːni/","part":"n.","meaning":"旅途，旅行","topic":"出行旅游&环境天气","level":"B",
   "s1":"The **journey** from London to Paris takes two hours.","s1c":"从伦敦到巴黎的旅程需要两个小时。",
   "s2":"We had a long **journey** by train to the coast.","s2c":"我们乘火车去海边进行了漫长的旅程。"},

  {"id":67,"word":"leave","phonetic":"/liːv/","part":"v.","meaning":"离开，出发","topic":"出行旅游&环境天气","level":"B",
   "s1":"The bus **leaves** at half past eight.","s1c":"公共汽车八点半出发。",
   "s2":"We **left** home early to catch the train.","s2c":"我们早早离开家去赶火车。"},

  {"id":68,"word":"mountain","phonetic":"/ˈmaʊntɪn/","part":"n.","meaning":"山","topic":"出行旅游&环境天气","level":"B",
   "s1":"We went hiking in the **mountains** last summer.","s1c":"去年夏天我们去山里徒步。",
   "s2":"The **mountain** is covered with snow in winter.","s2c":"冬天这座山被雪覆盖着。"},

  {"id":69,"word":"path","phonetic":"/pɑːθ/","part":"n.","meaning":"小路","topic":"出行旅游&环境天气","level":"B",
   "s1":"Follow the **path** through the park.","s1c":"沿着穿过公园的小路走。",
   "s2":"There is a narrow **path** along the river.","s2c":"沿着河边有一条狭窄的小路。"},

  {"id":70,"word":"railway","phonetic":"/ˈreɪlweɪ/","part":"n.","meaning":"铁路","topic":"出行旅游&环境天气","level":"B",
   "s1":"The **railway** station is ten minutes away.","s1c":"火车站距离这里十分钟。",
   "s2":"We crossed the **railway** bridge on our walk.","s2c":"我们散步时穿越了铁路桥。"},

  {"id":71,"word":"route","phonetic":"/ruːt/","part":"n.","meaning":"路线","topic":"出行旅游&环境天气","level":"B",
   "s1":"This is the fastest **route** to the school.","s1c":"这是去学校最快的路线。",
   "s2":"We planned our **route** on a map before the trip.","s2c":"旅行前我们在地图上规划了路线。"},

  {"id":72,"word":"station","phonetic":"/ˈsteɪʃn/","part":"n.","meaning":"车站","topic":"出行旅游&环境天气","level":"B",
   "s1":"Meet me at the bus **station** at three o'clock.","s1c":"三点钟在公共汽车站见我。",
   "s2":"The train **station** is very busy on Mondays.","s2c":"火车站在周一非常繁忙。"},

  {"id":73,"word":"storm","phonetic":"/stɔːm/","part":"n.","meaning":"暴风雨","topic":"出行旅游&环境天气","level":"B",
   "s1":"There was a big **storm** last night.","s1c":"昨晚有一场大暴风雨。",
   "s2":"The **storm** made it impossible to go outside.","s2c":"暴风雨使得我们无法外出。"},

  {"id":74,"word":"tourist","phonetic":"/ˈtʊərɪst/","part":"n.","meaning":"游客","topic":"出行旅游&环境天气","level":"B",
   "s1":"Many **tourists** visit the castle every year.","s1c":"每年有许多游客参观这座城堡。",
   "s2":"The **tourist** map shows all the main sights.","s2c":"游客地图显示了所有主要景点。"},

  {"id":75,"word":"traffic","phonetic":"/ˈtræfɪk/","part":"n.","meaning":"交通","topic":"出行旅游&环境天气","level":"B",
   "s1":"There is a lot of **traffic** in the city centre.","s1c":"市中心有很多交通拥挤。",
   "s2":"The bus was late because of heavy **traffic**.","s2c":"公共汽车因为交通拥堵而晚点了。"},

  {"id":76,"word":"travel","phonetic":"/ˈtrævl/","part":"v.","meaning":"旅行","topic":"出行旅游&环境天气","level":"B",
   "s1":"I would love to **travel** around the world.","s1c":"我很想环游世界。",
   "s2":"We **travelled** by train to visit our grandparents.","s2c":"我们乘火车去看望祖父母。"},

  {"id":77,"word":"weather","phonetic":"/ˈweðə/","part":"n.","meaning":"天气","topic":"出行旅游&环境天气","level":"B",
   "s1":"What is the **weather** like today?","s1c":"今天天气怎么样？",
   "s2":"The **weather** was warm and sunny during our holiday.","s2c":"假期期间天气温暖而晴朗。"},

  {"id":78,"word":"wind","phonetic":"/wɪnd/","part":"n.","meaning":"风","topic":"出行旅游&环境天气","level":"B",
   "s1":"The **wind** is very strong today.","s1c":"今天风很大。",
   "s2":"A cold **wind** blew across the playground.","s2c":"一阵冷风吹过操场。"},

  {"id":79,"word":"windy","phonetic":"/ˈwɪndi/","part":"adj.","meaning":"刮风的","topic":"出行旅游&环境天气","level":"B",
   "s1":"It is very **windy** today – hold your hat!","s1c":"今天风很大——抓住你的帽子！",
   "s2":"We could not fly our kite because it was too **windy**.","s2c":"因为风太大，我们无法放风筝。"},

  # ── 兴趣爱好&健康情绪 ──
  {"id":80,"word":"activity","phonetic":"/ækˈtɪvɪti/","part":"n.","meaning":"活动","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"Swimming is my favourite after-school **activity**.","s1c":"游泳是我最喜欢的课外活动。",
   "s2":"The school has many **activities** for students.","s2c":"学校为学生提供很多活动。"},

  {"id":81,"word":"artist","phonetic":"/ˈɑːtɪst/","part":"n.","meaning":"艺术家，画家","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"She wants to be an **artist** when she grows up.","s1c":"她长大后想成为一名艺术家。",
   "s2":"The **artist** painted a beautiful picture of the sea.","s2c":"这位艺术家画了一幅美丽的海景画。"},

  {"id":82,"word":"celebrate","phonetic":"/ˈselɪbreɪt/","part":"v.","meaning":"庆祝","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"We **celebrate** birthdays with a cake and songs.","s1c":"我们用蛋糕和歌曲庆祝生日。",
   "s2":"They **celebrated** the New Year with fireworks.","s2c":"他们用烟火庆祝新年。"},

  {"id":83,"word":"concert","phonetic":"/ˈkɒnsət/","part":"n.","meaning":"音乐会","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"We went to a music **concert** last Saturday.","s1c":"上周六我们去看了一场音乐会。",
   "s2":"The school **concert** was really wonderful.","s2c":"学校音乐会真的非常精彩。"},

  {"id":84,"word":"dance","phonetic":"/dɑːns/","part":"v.","meaning":"跳舞","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"I love to **dance** to pop music.","s1c":"我喜欢随着流行音乐跳舞。",
   "s2":"She **danced** at the school show last week.","s2c":"她上周在学校演出中跳舞了。"},

  {"id":85,"word":"exercise","phonetic":"/ˈeksəsaɪz/","part":"n./v.","meaning":"锻炼","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"**Exercise** is very important for good health.","s1c":"锻炼对健康非常重要。",
   "s2":"She **exercises** every morning before school.","s2c":"她每天早上上学前锻炼。"},

  {"id":86,"word":"festival","phonetic":"/ˈfestɪvl/","part":"n.","meaning":"节日","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"My favourite **festival** is the Spring Festival.","s1c":"我最喜欢的节日是春节。",
   "s2":"There is a music **festival** in our town every summer.","s2c":"我们镇每年夏天都有音乐节。"},

  {"id":87,"word":"hobby","phonetic":"/ˈhɒbi/","part":"n.","meaning":"爱好","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"My **hobby** is collecting stamps and postcards.","s1c":"我的爱好是收集邮票和明信片。",
   "s2":"What is your favourite **hobby** after school?","s2c":"你课后最喜欢的爱好是什么？"},

  {"id":88,"word":"healthy","phonetic":"/ˈhelθi/","part":"adj.","meaning":"健康的","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"Eating fruit and vegetables keeps you **healthy**.","s1c":"吃水果和蔬菜能让你保持健康。",
   "s2":"She lives a **healthy** life and goes running every day.","s2c":"她过着健康的生活，每天跑步。"},

  {"id":89,"word":"interested","phonetic":"/ˈɪntrəstɪd/","part":"adj.","meaning":"感兴趣的","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"I am very **interested** in learning about animals.","s1c":"我对学习动物知识非常感兴趣。",
   "s2":"Are you **interested** in joining the art club?","s2c":"你有兴趣加入美术俱乐部吗？"},

  {"id":90,"word":"match","phonetic":"/mætʃ/","part":"n.","meaning":"比赛","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"We watched a football **match** on Saturday.","s1c":"我们星期六看了一场足球比赛。",
   "s2":"Our school won the basketball **match** yesterday.","s2c":"我们学校昨天赢了篮球比赛。"},

  {"id":91,"word":"music","phonetic":"/ˈmjuːzɪk/","part":"n.","meaning":"音乐","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"I listen to **music** every evening before bed.","s1c":"我每晚睡前听音乐。",
   "s2":"She plays **music** and dances at the school show.","s2c":"她在学校演出中演奏音乐并跳舞。"},

  {"id":92,"word":"relax","phonetic":"/rɪˈlæks/","part":"v.","meaning":"放松","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"I like to **relax** by reading after school.","s1c":"我喜欢放学后通过读书来放松。",
   "s2":"**Relax** and take a deep breath before the test.","s2c":"考试前放松一下，深呼吸。"},

  {"id":93,"word":"sport","phonetic":"/spɔːt/","part":"n.","meaning":"运动","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"My favourite **sport** is swimming.","s1c":"我最喜欢的运动是游泳。",
   "s2":"She plays **sport** every day to stay fit.","s2c":"她每天运动以保持健康。"},

  {"id":94,"word":"talent","phonetic":"/ˈtælənt/","part":"n.","meaning":"天赋","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"She has a great **talent** for singing.","s1c":"她有很高的唱歌天赋。",
   "s2":"Everyone has a special **talent** of their own.","s2c":"每个人都有自己特别的天赋。"},

  {"id":95,"word":"tired","phonetic":"/ˈtaɪəd/","part":"adj.","meaning":"疲惫的","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"I feel very **tired** after my swimming lesson.","s1c":"游泳课后我感到非常疲惫。",
   "s2":"She was **tired** but still finished her homework.","s2c":"她虽然很累，但还是完成了作业。"},

  {"id":96,"word":"volunteer","phonetic":"/ˌvɒlənˈtɪə/","part":"n.","meaning":"志愿者","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"She is a **volunteer** at the local library.","s1c":"她是当地图书馆的志愿者。",
   "s2":"Many **volunteers** helped clean the park.","s2c":"许多志愿者帮助清洁公园。"},

  {"id":97,"word":"win","phonetic":"/wɪn/","part":"v.","meaning":"赢得，获胜","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"Our team **won** the football match last weekend.","s1c":"我们队上周末赢了足球比赛。",
   "s2":"She **won** first prize in the art competition.","s2c":"她在美术比赛中获得了一等奖。"},

  {"id":98,"word":"wonderful","phonetic":"/ˈwʌndəfl/","part":"adj.","meaning":"极好的","topic":"兴趣爱好&健康情绪","level":"B",
   "s1":"We had a **wonderful** time at the festival.","s1c":"我们在节日上度过了美好的时光。",
   "s2":"What a **wonderful** surprise to see you here!","s2c":"在这里见到你真是太惊喜了！"},

  # ── 人物&状态 ──
  {"id":99,"word":"alone","phonetic":"/əˈləʊn/","part":"adj.","meaning":"独自的，单独的","topic":"人物&状态","level":"B",
   "s1":"She sat **alone** in the classroom after school.","s1c":"放学后她独自坐在教室里。",
   "s2":"I don't like going to the cinema **alone**.","s2c":"我不喜欢独自去电影院。"},

  {"id":100,"word":"angry","phonetic":"/ˈæŋɡri/","part":"adj.","meaning":"生气的","topic":"人物&状态","level":"B",
   "s1":"My dad was **angry** when I came home late.","s1c":"我回家晚了，爸爸很生气。",
   "s2":"She was **angry** because I lost her book.","s2c":"她很生气，因为我弄丢了她的书。"},

  {"id":101,"word":"beautiful","phonetic":"/ˈbjuːtɪfl/","part":"adj.","meaning":"美丽的，漂亮的","topic":"人物&状态","level":"B",
   "s1":"She wore a **beautiful** dress to the party.","s1c":"她穿了一件漂亮的裙子去派对。",
   "s2":"The flowers in the garden are **beautiful** in spring.","s2c":"花园里的花在春天很美丽。"},

  {"id":102,"word":"bored","phonetic":"/bɔːd/","part":"adj.","meaning":"无聊的","topic":"人物&状态","level":"B",
   "s1":"I felt **bored** because there was nothing to do.","s1c":"我感到无聊，因为没有什么事情可做。",
   "s2":"She was **bored** at home during the holidays.","s2c":"假期在家时她感到无聊。"},

  {"id":103,"word":"bright","phonetic":"/braɪt/","part":"adj.","meaning":"明亮的，聪明的","topic":"人物&状态","level":"B",
   "s1":"The sun is very **bright** this morning.","s1c":"今天早上阳光非常明亮。",
   "s2":"She is a **bright** student who loves reading.","s2c":"她是一个聪明的学生，喜欢读书。"},

  {"id":104,"word":"clean","phonetic":"/kliːn/","part":"adj./v.","meaning":"干净的/打扫","topic":"人物&状态","level":"B",
   "s1":"Please keep your desk **clean** and tidy.","s1c":"请保持你的桌子干净整洁。",
   "s2":"We **cleaned** the classroom before going home.","s2c":"我们回家前打扫了教室。"},

  {"id":105,"word":"cold","phonetic":"/kəʊld/","part":"adj.","meaning":"寒冷的","topic":"人物&状态","level":"B",
   "s1":"It is very **cold** outside today.","s1c":"今天外面非常寒冷。",
   "s2":"Put on a coat because it is **cold**.","s2c":"穿上外套，因为天气很冷。"},

  {"id":106,"word":"cool","phonetic":"/kuːl/","part":"adj.","meaning":"凉爽的，酷的","topic":"人物&状态","level":"B",
   "s1":"The weather is nice and **cool** in autumn.","s1c":"秋天天气凉爽宜人。",
   "s2":"That is a really **cool** bike!","s2c":"那辆自行车真的很酷！"},

  {"id":107,"word":"dangerous","phonetic":"/ˈdeɪndʒərəs/","part":"adj.","meaning":"危险的","topic":"人物&状态","level":"B",
   "s1":"It is **dangerous** to run near the swimming pool.","s1c":"在游泳池附近跑步是危险的。",
   "s2":"Swimming in the sea alone can be **dangerous**.","s2c":"独自在海里游泳可能很危险。"},

  {"id":108,"word":"dark","phonetic":"/dɑːk/","part":"adj.","meaning":"黑暗的","topic":"人物&状态","level":"B",
   "s1":"It is very **dark** outside at night.","s1c":"夜里外面非常黑暗。",
   "s2":"She is afraid of the **dark** and uses a night light.","s2c":"她怕黑，所以用夜灯。"},

  {"id":109,"word":"different","phonetic":"/ˈdɪfrənt/","part":"adj.","meaning":"不同的","topic":"人物&状态","level":"B",
   "s1":"My sister and I have very **different** hobbies.","s1c":"我和姐姐有非常不同的爱好。",
   "s2":"These two books are **different** from each other.","s2c":"这两本书彼此不同。"},

  {"id":110,"word":"difficult","phonetic":"/ˈdɪfɪkəlt/","part":"adj.","meaning":"困难的","topic":"人物&状态","level":"B",
   "s1":"The maths test was very **difficult** today.","s1c":"今天的数学考试非常难。",
   "s2":"Learning a new language can be **difficult** at first.","s2c":"学习一门新语言起初可能很困难。"},

  {"id":111,"word":"dirty","phonetic":"/ˈdɜːti/","part":"adj.","meaning":"脏的","topic":"人物&状态","level":"B",
   "s1":"My shoes are very **dirty** after playing outside.","s1c":"在外面玩耍后我的鞋子很脏。",
   "s2":"Please wash your hands because they are **dirty**.","s2c":"请洗手，因为你的手很脏。"},

  {"id":112,"word":"easy","phonetic":"/ˈiːzi/","part":"adj.","meaning":"容易的","topic":"人物&状态","level":"B",
   "s1":"The first question in the test was very **easy**.","s1c":"考试中的第一道题非常容易。",
   "s2":"This recipe is very **easy** to follow.","s2c":"这个食谱非常容易跟着做。"},

  {"id":113,"word":"excited","phonetic":"/ɪkˈsaɪtɪd/","part":"adj.","meaning":"兴奋的","topic":"人物&状态","level":"B",
   "s1":"I am very **excited** about my birthday party.","s1c":"我对生日派对非常兴奋。",
   "s2":"She was **excited** when she heard the good news.","s2c":"当她听到好消息时非常兴奋。"},

  {"id":114,"word":"famous","phonetic":"/ˈfeɪməs/","part":"adj.","meaning":"著名的","topic":"人物&状态","level":"B",
   "s1":"Paris is **famous** for its beautiful buildings.","s1c":"巴黎以其美丽的建筑而闻名。",
   "s2":"She is a **famous** singer all over the world.","s2c":"她是全球知名的歌手。"},

  {"id":115,"word":"fast","phonetic":"/fɑːst/","part":"adj./adv.","meaning":"快的，快速地","topic":"人物&状态","level":"B",
   "s1":"She is the **fastest** runner in our class.","s1c":"她是我们班跑得最快的。",
   "s2":"The car drove very **fast** on the motorway.","s2c":"汽车在高速公路上开得很快。"},

  {"id":116,"word":"fat","phonetic":"/fæt/","part":"adj.","meaning":"胖的，肥的","topic":"人物&状态","level":"B",
   "s1":"The **fat** cat sat on the warm sofa.","s1c":"那只胖猫坐在温暖的沙发上。",
   "s2":"Eating too much sugar can make you **fat**.","s2c":"吃太多糖会让你变胖。"},

  {"id":117,"word":"fit","phonetic":"/fɪt/","part":"adj.","meaning":"健康的，合适的","topic":"人物&状态","level":"B",
   "s1":"She goes running every day to stay **fit**.","s1c":"她每天跑步以保持健康。",
   "s2":"You need to get **fit** before the swimming race.","s2c":"你需要在游泳比赛前保持健康。"},

  {"id":118,"word":"funny","phonetic":"/ˈfʌni/","part":"adj.","meaning":"有趣的，滑稽的","topic":"人物&状态","level":"B",
   "s1":"My dad always tells **funny** jokes at dinner.","s1c":"我爸爸总是在晚饭时讲有趣的笑话。",
   "s2":"The cartoon was very **funny** and we all laughed.","s2c":"这部卡通片非常有趣，我们都笑了。"},

  # ── 学习&工作动作 ──
  {"id":119,"word":"add","phonetic":"/æd/","part":"v.","meaning":"添加，增加","topic":"学习&工作动作","level":"B",
   "s1":"**Add** some salt to the soup, please.","s1c":"请往汤里加点盐。",
   "s2":"She **added** her name to the list.","s2c":"她把名字加到了名单上。"},

  {"id":120,"word":"allow","phonetic":"/əˈlaʊ/","part":"v.","meaning":"允许","topic":"学习&工作动作","level":"B",
   "s1":"We are not **allowed** to use phones in class.","s1c":"我们在课堂上不允许使用手机。",
   "s2":"My parents **allow** me to watch TV for one hour.","s2c":"我父母允许我看一小时电视。"},

  {"id":121,"word":"answer","phonetic":"/ˈɑːnsə/","part":"v.","meaning":"回答","topic":"学习&工作动作","level":"B",
   "s1":"Please **answer** all the questions in the test.","s1c":"请回答考试中的所有问题。",
   "s2":"She **answered** the teacher's question correctly.","s2c":"她正确回答了老师的问题。"},

  {"id":122,"word":"ask","phonetic":"/ɑːsk/","part":"v.","meaning":"询问，要求","topic":"学习&工作动作","level":"B",
   "s1":"You can **ask** the teacher if you do not understand.","s1c":"如果你不明白，可以问老师。",
   "s2":"She **asked** her friend for help with the homework.","s2c":"她请朋友帮助做作业。"},

  {"id":123,"word":"believe","phonetic":"/bɪˈliːv/","part":"v.","meaning":"相信","topic":"学习&工作动作","level":"B",
   "s1":"I **believe** you can pass the KET exam.","s1c":"我相信你能通过KET考试。",
   "s2":"Do you **believe** this story is true?","s2c":"你相信这个故事是真的吗？"},

  {"id":124,"word":"break","phonetic":"/breɪk/","part":"v.","meaning":"打破，弄坏","topic":"学习&工作动作","level":"B",
   "s1":"Be careful! Don't **break** the glasses.","s1c":"小心！不要打破玻璃杯。",
   "s2":"She **broke** her arm when she fell off her bike.","s2c":"她从自行车上摔下来，摔断了手臂。"},

  {"id":125,"word":"bring","phonetic":"/brɪŋ/","part":"v.","meaning":"带来，拿来","topic":"学习&工作动作","level":"B",
   "s1":"Please **bring** your book to class tomorrow.","s1c":"请明天把你的书带到课上。",
   "s2":"She **brought** some cakes to share with the class.","s2c":"她带了一些蛋糕和全班同学分享。"},

  {"id":126,"word":"build","phonetic":"/bɪld/","part":"v.","meaning":"建造，搭建","topic":"学习&工作动作","level":"B",
   "s1":"We **built** a sandcastle on the beach.","s1c":"我们在海滩上建造了一座沙堡。",
   "s2":"He wants to **build** a treehouse in the garden.","s2c":"他想在花园里搭建一个树屋。"},

  {"id":127,"word":"call","phonetic":"/kɔːl/","part":"v.","meaning":"称呼，打电话","topic":"学习&工作动作","level":"B",
   "s1":"She **called** her grandmother every Sunday.","s1c":"她每个星期天给祖母打电话。",
   "s2":"What do you **call** this animal in English?","s2c":"这种动物用英语怎么称呼？"},

  {"id":128,"word":"carry","phonetic":"/ˈkæri/","part":"v.","meaning":"携带，搬运","topic":"学习&工作动作","level":"B",
   "s1":"Can you **carry** this heavy bag for me?","s1c":"你能帮我搬这个重包吗？",
   "s2":"She **carried** her lunch in a small bag.","s2c":"她用一个小包带着她的午饭。"},

  {"id":129,"word":"catch","phonetic":"/kætʃ/","part":"v.","meaning":"抓住，接住","topic":"学习&工作动作","level":"B",
   "s1":"She **caught** the ball and threw it back.","s1c":"她接住球后又把球扔了回去。",
   "s2":"Hurry up or you will miss the bus – we have to **catch** it!","s2c":"快点，不然你会错过公共汽车的，我们得赶上它！"},

  {"id":130,"word":"change","phonetic":"/tʃeɪndʒ/","part":"v.","meaning":"改变，更换","topic":"学习&工作动作","level":"B",
   "s1":"I will **change** my clothes after school.","s1c":"我放学后会换衣服。",
   "s2":"The weather can **change** very quickly in spring.","s2c":"春天天气变化很快。"},

  {"id":131,"word":"check","phonetic":"/tʃek/","part":"v.","meaning":"检查，核对","topic":"学习&工作动作","level":"B",
   "s1":"Please **check** your answers before handing in the test.","s1c":"交卷前请检查你的答案。",
   "s2":"She **checked** her bag to make sure she had her keys.","s2c":"她检查了包以确保带了钥匙。"},

  {"id":132,"word":"close","phonetic":"/kləʊz/","part":"v.","meaning":"关闭","topic":"学习&工作动作","level":"B",
   "s1":"Please **close** the door when you leave.","s1c":"离开时请关门。",
   "s2":"The shop **closes** at six o'clock in the evening.","s2c":"商店晚上六点关门。"},

  {"id":133,"word":"collect","phonetic":"/kəˈlekt/","part":"v.","meaning":"收集，采集","topic":"学习&工作动作","level":"B",
   "s1":"He loves to **collect** football cards.","s1c":"他喜欢收集足球卡。",
   "s2":"We **collected** leaves in the park last autumn.","s2c":"去年秋天我们在公园里收集了树叶。"},

  {"id":134,"word":"come","phonetic":"/kʌm/","part":"v.","meaning":"来，来到","topic":"学习&工作动作","level":"B",
   "s1":"Please **come** to my birthday party on Saturday.","s1c":"请来参加我星期六的生日派对。",
   "s2":"She **came** home late after her dance class.","s2c":"舞蹈课后她很晚才回家。"},

  {"id":135,"word":"cook","phonetic":"/kʊk/","part":"v.","meaning":"烹饪，做饭","topic":"学习&工作动作","level":"B",
   "s1":"My mum **cooks** dinner for us every evening.","s1c":"我妈妈每天晚上为我们做晚饭。",
   "s2":"I **cooked** pasta for the first time last week.","s2c":"上周我第一次做了意大利面。"},

  {"id":136,"word":"cut","phonetic":"/kʌt/","part":"v.","meaning":"切，割","topic":"学习&工作动作","level":"B",
   "s1":"Please **cut** the bread into small pieces.","s1c":"请把面包切成小块。",
   "s2":"She **cut** some flowers from the garden for the table.","s2c":"她从花园里剪了一些花放在桌子上。"},

  {"id":137,"word":"decide","phonetic":"/dɪˈsaɪd/","part":"v.","meaning":"决定","topic":"学习&工作动作","level":"B",
   "s1":"We **decided** to go to the park after lunch.","s1c":"我们决定午饭后去公园。",
   "s2":"Have you **decided** what to study at university?","s2c":"你决定好大学要学什么了吗？"},

  {"id":138,"word":"do","phonetic":"/duː/","part":"v.","meaning":"做，干","topic":"学习&工作动作","level":"B",
   "s1":"I always **do** my homework before dinner.","s1c":"我总是在晚饭前做作业。",
   "s2":"What did you **do** last weekend?","s2c":"你上周末做了什么？"},

  # ── 生活&饮食购物 ──
  {"id":139,"word":"drink","phonetic":"/drɪŋk/","part":"v./n.","meaning":"喝/饮品","topic":"生活&饮食购物","level":"B",
   "s1":"You should **drink** eight glasses of water each day.","s1c":"你每天应该喝八杯水。",
   "s2":"What would you like to **drink** with your meal?","s2c":"用餐时你想喝什么？"},

  {"id":140,"word":"drive","phonetic":"/draɪv/","part":"v.","meaning":"驾驶，开车","topic":"生活&饮食购物","level":"B",
   "s1":"My dad **drives** me to school every morning.","s1c":"我爸爸每天早上开车送我上学。",
   "s2":"She learned to **drive** when she was eighteen.","s2c":"她十八岁时学会了开车。"},

  {"id":141,"word":"eat","phonetic":"/iːt/","part":"v.","meaning":"吃","topic":"生活&饮食购物","level":"B",
   "s1":"We **eat** breakfast together every morning.","s1c":"我们每天早上一起吃早饭。",
   "s2":"She **ate** a big bowl of noodles for lunch.","s2c":"她午饭吃了一大碗面条。"},

  {"id":142,"word":"feed","phonetic":"/fiːd/","part":"v.","meaning":"喂养，喂食","topic":"生活&饮食购物","level":"B",
   "s1":"I **feed** my pet cat twice a day.","s1c":"我每天喂猫咪两次。",
   "s2":"She **fed** the ducks at the park last Sunday.","s2c":"上周日她在公园喂了鸭子。"},

  {"id":143,"word":"fill","phonetic":"/fɪl/","part":"v.","meaning":"填满，装满","topic":"生活&饮食购物","level":"B",
   "s1":"Please **fill** the bottle with cold water.","s1c":"请把瓶子装满冷水。",
   "s2":"She **filled** the bag with books and left for school.","s2c":"她把书装进包里，然后去上学了。"},

  {"id":144,"word":"find","phonetic":"/faɪnd/","part":"v.","meaning":"找到，发现","topic":"生活&饮食购物","level":"B",
   "s1":"I cannot **find** my school bag anywhere.","s1c":"我到处找不到我的书包。",
   "s2":"She **found** a ten pound note on the street.","s2c":"她在街上发现了一张十英镑的钞票。"},

  {"id":145,"word":"fix","phonetic":"/fɪks/","part":"v.","meaning":"修理，安装","topic":"生活&饮食购物","level":"B",
   "s1":"Dad **fixed** my bike after it broke.","s1c":"自行车坏了之后，爸爸帮我修好了。",
   "s2":"Can you **fix** the broken chair in the kitchen?","s2c":"你能修好厨房里那把坏椅子吗？"},

  {"id":146,"word":"fly","phonetic":"/flaɪ/","part":"v.","meaning":"飞，飞行","topic":"生活&饮食购物","level":"B",
   "s1":"Birds **fly** south in autumn.","s1c":"鸟在秋天往南飞。",
   "s2":"We **flew** to Spain for our summer holiday.","s2c":"我们乘飞机去西班牙度暑假。"},

  {"id":147,"word":"forgive","phonetic":"/fəˈɡɪv/","part":"v.","meaning":"原谅，宽恕","topic":"生活&饮食购物","level":"B",
   "s1":"Please **forgive** me – I did not mean to be late.","s1c":"请原谅我——我不是故意迟到的。",
   "s2":"She **forgave** her friend after their argument.","s2c":"她原谅了争吵后的朋友。"},

  {"id":148,"word":"get","phonetic":"/ɡet/","part":"v.","meaning":"得到，获得","topic":"生活&饮食购物","level":"B",
   "s1":"I **got** a new book for my birthday.","s1c":"我生日收到了一本新书。",
   "s2":"Can you **get** some milk from the shop?","s2c":"你能去商店买些牛奶吗？"},

  {"id":149,"word":"give","phonetic":"/ɡɪv/","part":"v.","meaning":"给，赠送","topic":"生活&饮食购物","level":"B",
   "s1":"My grandmother **gave** me a lovely gift.","s1c":"我祖母给了我一份可爱的礼物。",
   "s2":"Please **give** me your homework book.","s2c":"请把你的作业本给我。"},

  {"id":150,"word":"go","phonetic":"/ɡəʊ/","part":"v.","meaning":"去，走","topic":"生活&饮食购物","level":"B",
   "s1":"We **go** to school by bus every morning.","s1c":"我们每天早上坐公共汽车上学。",
   "s2":"Let's **go** to the park after lunch.","s2c":"午饭后我们去公园吧。"},

  {"id":151,"word":"grow","phonetic":"/ɡrəʊ/","part":"v.","meaning":"生长，成长","topic":"生活&饮食购物","level":"B",
   "s1":"We **grow** tomatoes in our garden every summer.","s1c":"我们每年夏天在花园里种番茄。",
   "s2":"Children **grow** very quickly in their first few years.","s2c":"孩子在最初几年里成长非常迅速。"},

  {"id":152,"word":"hang","phonetic":"/hæŋ/","part":"v.","meaning":"悬挂，吊起","topic":"生活&饮食购物","level":"B",
   "s1":"Please **hang** your coat on the hook.","s1c":"请把你的外套挂在钩子上。",
   "s2":"She **hung** a picture of her family on the wall.","s2c":"她把一张家庭照片挂在墙上。"},

  {"id":153,"word":"have","phonetic":"/hæv/","part":"v.","meaning":"有，拥有","topic":"生活&饮食购物","level":"B",
   "s1":"I **have** two sisters and one brother.","s1c":"我有两个姐妹和一个兄弟。",
   "s2":"Do you **have** a pen I can borrow?","s2c":"你有钢笔可以借给我吗？"},

  {"id":154,"word":"hear","phonetic":"/hɪə/","part":"v.","meaning":"听见，听到","topic":"生活&饮食购物","level":"B",
   "s1":"Can you **hear** the music from next door?","s1c":"你能听到隔壁的音乐吗？",
   "s2":"She **heard** a strange noise in the garden.","s2c":"她听到花园里有奇怪的声音。"},

  {"id":155,"word":"help","phonetic":"/help/","part":"v.","meaning":"帮助","topic":"生活&饮食购物","level":"B",
   "s1":"Can you **help** me carry this heavy bag?","s1c":"你能帮我搬这个重包吗？",
   "s2":"She always **helps** her little brother with his reading.","s2c":"她总是帮助弟弟练习阅读。"},

  {"id":156,"word":"hide","phonetic":"/haɪd/","part":"v.","meaning":"隐藏，躲藏","topic":"生活&饮食购物","level":"B",
   "s1":"The cat **hid** behind the sofa.","s1c":"猫躲在沙发后面。",
   "s2":"I **hid** the birthday present under my bed.","s2c":"我把生日礼物藏在床底下。"},

  {"id":157,"word":"hit","phonetic":"/hɪt/","part":"v.","meaning":"打，撞击","topic":"生活&饮食购物","level":"B",
   "s1":"She **hit** the ball very hard with her racket.","s1c":"她用球拍用力打了球。",
   "s2":"The ball **hit** the window and broke it.","s2c":"球打到了窗户，把窗户打碎了。"},

  {"id":158,"word":"hold","phonetic":"/həʊld/","part":"v.","meaning":"拿着，握住","topic":"生活&饮食购物","level":"B",
   "s1":"**Hold** my hand when we cross the road.","s1c":"过马路时握住我的手。",
   "s2":"She **held** the baby carefully in her arms.","s2c":"她小心地把婴儿抱在怀里。"},

  # ── 出行&环境天气 ──
  {"id":159,"word":"home","phonetic":"/həʊm/","part":"n.","meaning":"家","topic":"出行&环境天气","level":"C",
   "s1":"I walked **home** from school with my friend.","s1c":"我和朋友一起从学校走回家。",
   "s2":"There is no place like **home**.","s2c":"家是最温暖的地方。"},

  {"id":160,"word":"hospital","phonetic":"/ˈhɒspɪtl/","part":"n.","meaning":"医院","topic":"出行&环境天气","level":"C",
   "s1":"She went to the **hospital** to visit her grandmother.","s1c":"她去医院探望祖母。",
   "s2":"The **hospital** is near the town centre.","s2c":"医院在市中心附近。"},

  {"id":161,"word":"hotel","phonetic":"/həʊˈtel/","part":"n.","meaning":"酒店，旅馆","topic":"出行&环境天气","level":"C",
   "s1":"We stayed in a **hotel** near the beach.","s1c":"我们住在海边附近的酒店。",
   "s2":"The **hotel** has a lovely swimming pool.","s2c":"这家酒店有一个漂亮的游泳池。"},

  {"id":162,"word":"house","phonetic":"/haʊs/","part":"n.","meaning":"房子，住宅","topic":"出行&环境天气","level":"C",
   "s1":"My **house** has three bedrooms and a garden.","s1c":"我家有三间卧室和一个花园。",
   "s2":"They painted their **house** yellow last summer.","s2c":"他们去年夏天把房子漆成黄色。"},

  {"id":163,"word":"lake","phonetic":"/leɪk/","part":"n.","meaning":"湖","topic":"出行&环境天气","level":"C",
   "s1":"We went fishing at the **lake** at the weekend.","s1c":"我们周末去湖边钓鱼。",
   "s2":"The **lake** is very beautiful in the morning.","s2c":"湖在早上非常美丽。"},

  {"id":164,"word":"land","phonetic":"/lænd/","part":"n.","meaning":"陆地，土地","topic":"出行&环境天气","level":"C",
   "s1":"The plane will **land** in twenty minutes.","s1c":"飞机将在二十分钟后降落。",
   "s2":"After two weeks at sea, they saw **land**.","s2c":"在海上漂了两周后，他们看到了陆地。"},

  {"id":165,"word":"large","phonetic":"/lɑːdʒ/","part":"adj.","meaning":"大的，巨大的","topic":"出行&环境天气","level":"C",
   "s1":"They live in a **large** house with a big garden.","s1c":"他们住在一栋有大花园的大房子里。",
   "s2":"There is a **large** supermarket near our school.","s2c":"我们学校附近有一家大超市。"},

  {"id":166,"word":"last","phonetic":"/lɑːst/","part":"adj./v.","meaning":"最后的，上一个的/持续","topic":"出行&环境天气","level":"C",
   "s1":"The **last** bus leaves at ten o'clock at night.","s1c":"最后一班公共汽车晚上十点出发。",
   "s2":"The football match **lasted** for ninety minutes.","s2c":"足球比赛持续了九十分钟。"},

  {"id":167,"word":"late","phonetic":"/leɪt/","part":"adj.","meaning":"晚的，迟到的","topic":"出行&环境天气","level":"C",
   "s1":"The train was **late** because of the storm.","s1c":"由于暴风雨，火车晚点了。",
   "s2":"Please don't be **late** for school tomorrow.","s2c":"明天上学请不要迟到。"},

  {"id":168,"word":"left","phonetic":"/left/","part":"adj.","meaning":"左边的","topic":"出行&环境天气","level":"C",
   "s1":"Turn **left** at the traffic lights.","s1c":"在交通灯处左转。",
   "s2":"The school is on the **left** side of the road.","s2c":"学校在路的左边。"},

  {"id":169,"word":"light","phonetic":"/laɪt/","part":"n./adj.","meaning":"灯，光线/轻的","topic":"出行&环境天气","level":"C",
   "s1":"Please turn on the **light** – it is too dark.","s1c":"请开灯——太黑了。",
   "s2":"This bag is very **light** and easy to carry.","s2c":"这个包很轻，容易携带。"},

  {"id":170,"word":"like","phonetic":"/laɪk/","part":"v./prep.","meaning":"喜欢/像","topic":"出行&环境天气","level":"C",
   "s1":"I **like** reading books about animals.","s1c":"我喜欢读关于动物的书。",
   "s2":"She runs **like** the wind – she is so fast.","s2c":"她跑得像风一样——她真的很快。"},

  {"id":171,"word":"live","phonetic":"/lɪv/","part":"v.","meaning":"居住，生活","topic":"出行&环境天气","level":"C",
   "s1":"I **live** in a small town near London.","s1c":"我住在伦敦附近的一个小镇上。",
   "s2":"She has **lived** in the same house all her life.","s2c":"她一生都住在同一栋房子里。"},

  {"id":172,"word":"long","phonetic":"/lɒŋ/","part":"adj.","meaning":"长的，久的","topic":"出行&环境天气","level":"C",
   "s1":"It is a **long** walk from my house to the station.","s1c":"从我家到车站走路很长。",
   "s2":"She has very **long** hair and it is very beautiful.","s2c":"她有很长的头发，非常漂亮。"},

  {"id":173,"word":"look","phonetic":"/lʊk/","part":"v.","meaning":"看，看起来","topic":"出行&环境天气","level":"C",
   "s1":"**Look** at the birds in the sky!","s1c":"看天上的鸟！",
   "s2":"She **looks** very happy today.","s2c":"她今天看起来很开心。"},

  {"id":174,"word":"lose","phonetic":"/luːz/","part":"v.","meaning":"丢失，失去","topic":"出行&环境天气","level":"C",
   "s1":"I **lost** my keys somewhere in the house.","s1c":"我把钥匙丢在房子里某处了。",
   "s2":"Our team **lost** the match yesterday by one goal.","s2c":"我们队昨天以一球之差输了比赛。"},

  {"id":175,"word":"low","phonetic":"/ləʊ/","part":"adj.","meaning":"低的，矮的","topic":"出行&环境天气","level":"C",
   "s1":"The temperature is very **low** in winter.","s1c":"冬天气温非常低。",
   "s2":"Mind your head – that bridge is very **low**.","s2c":"注意你的头——那座桥非常低。"},

  {"id":176,"word":"make","phonetic":"/meɪk/","part":"v.","meaning":"制作，使","topic":"出行&环境天气","level":"C",
   "s1":"She **makes** her own breakfast every morning.","s1c":"她每天早上自己做早饭。",
   "s2":"Let's **make** a card for our teacher's birthday.","s2c":"我们来为老师的生日做张贺卡吧。"},

  {"id":177,"word":"map","phonetic":"/mæp/","part":"n.","meaning":"地图","topic":"出行&环境天气","level":"C",
   "s1":"We used a **map** to find our way in the city.","s1c":"我们用地图在城市里找路。",
   "s2":"She drew a **map** of our school for the new student.","s2c":"她为新同学画了一张学校地图。"},

  {"id":178,"word":"market","phonetic":"/ˈmɑːkɪt/","part":"n.","meaning":"市场，集市","topic":"出行&环境天气","level":"C",
   "s1":"Mum buys fresh vegetables at the **market**.","s1c":"妈妈在市场买新鲜蔬菜。",
   "s2":"The **market** opens every Saturday morning.","s2c":"市场每周六早上开放。"},

  # ── 兴趣&健康情绪 ──
  {"id":179,"word":"matter","phonetic":"/ˈmætə/","part":"n.","meaning":"事情，问题","topic":"兴趣&健康情绪","level":"C",
   "s1":"What is the **matter**? You look sad.","s1c":"怎么了？你看起来很难过。",
   "s2":"It does not **matter** if you make a small mistake.","s2c":"犯小错误没关系。"},

  {"id":180,"word":"may","phonetic":"/meɪ/","part":"modal v.","meaning":"可以，可能","topic":"兴趣&健康情绪","level":"C",
   "s1":"**May** I open the window, please?","s1c":"我可以打开窗户吗？",
   "s2":"It **may** rain this afternoon, so take an umbrella.","s2c":"今天下午可能下雨，所以带把伞。"},

  {"id":181,"word":"mean","phonetic":"/miːn/","part":"v.","meaning":"意思是，意味着","topic":"兴趣&健康情绪","level":"C",
   "s1":"What does this word **mean** in English?","s1c":"这个单词用英语是什么意思？",
   "s2":"I did not **mean** to hurt your feelings.","s2c":"我不是故意伤害你的感情的。"},

  {"id":182,"word":"meet","phonetic":"/miːt/","part":"v.","meaning":"遇见，见面","topic":"兴趣&健康情绪","level":"C",
   "s1":"I **meet** my friends at the park every Saturday.","s1c":"我每周六在公园见朋友。",
   "s2":"Nice to **meet** you! I'm Tom.","s2c":"很高兴认识你！我是Tom。"},

  {"id":183,"word":"milk","phonetic":"/mɪlk/","part":"n.","meaning":"牛奶","topic":"兴趣&健康情绪","level":"C",
   "s1":"I drink a glass of **milk** every morning.","s1c":"我每天早上喝一杯牛奶。",
   "s2":"Please add some **milk** to my tea.","s2c":"请在我的茶里加一些牛奶。"},

  {"id":184,"word":"mind","phonetic":"/maɪnd/","part":"v./n.","meaning":"介意/头脑，心思","topic":"兴趣&健康情绪","level":"C",
   "s1":"Do you **mind** if I sit here?","s1c":"你介意我坐这里吗？",
   "s2":"She has a very quick **mind** and learns fast.","s2c":"她头脑非常敏锐，学东西很快。"},

  {"id":185,"word":"mix","phonetic":"/mɪks/","part":"v.","meaning":"混合，搅拌","topic":"兴趣&健康情绪","level":"C",
   "s1":"**Mix** the flour and eggs to make a cake.","s1c":"把面粉和鸡蛋混合在一起做蛋糕。",
   "s2":"She **mixed** the colours to make a new shade.","s2c":"她把颜色混合在一起，调出了新的色调。"},

  {"id":186,"word":"money","phonetic":"/ˈmʌni/","part":"n.","meaning":"钱，金钱","topic":"兴趣&健康情绪","level":"C",
   "s1":"I save my **money** to buy a new book.","s1c":"我存钱买一本新书。",
   "s2":"She did not have enough **money** to buy the shoes.","s2c":"她没有足够的钱买那双鞋。"},

  {"id":187,"word":"month","phonetic":"/mʌnθ/","part":"n.","meaning":"月，月份","topic":"兴趣&健康情绪","level":"C",
   "s1":"My birthday is next **month**.","s1c":"我的生日在下个月。",
   "s2":"We have been studying KET for four **months**.","s2c":"我们已经学习KET四个月了。"},

  {"id":188,"word":"morning","phonetic":"/ˈmɔːnɪŋ/","part":"n.","meaning":"早上，上午","topic":"兴趣&健康情绪","level":"C",
   "s1":"I wake up early every **morning**.","s1c":"我每天早上都早起。",
   "s2":"She goes for a run in the **morning** before school.","s2c":"她上学前在早上跑步。"},

  {"id":189,"word":"mother","phonetic":"/ˈmʌðə/","part":"n.","meaning":"母亲，妈妈","topic":"兴趣&健康情绪","level":"C",
   "s1":"My **mother** cooks the best food in the world.","s1c":"我妈妈做的饭是世界上最好吃的。",
   "s2":"I gave my **mother** flowers on her birthday.","s2c":"我在妈妈生日时送了她鲜花。"},

  {"id":190,"word":"need","phonetic":"/niːd/","part":"v.","meaning":"需要","topic":"兴趣&健康情绪","level":"C",
   "s1":"I **need** to buy a new pencil case.","s1c":"我需要买一个新的铅笔盒。",
   "s2":"Do you **need** help with your homework?","s2c":"你需要帮助做作业吗？"},

  {"id":191,"word":"new","phonetic":"/njuː/","part":"adj.","meaning":"新的","topic":"兴趣&健康情绪","level":"C",
   "s1":"She got a **new** bicycle for her birthday.","s1c":"她生日收到了一辆新自行车。",
   "s2":"There is a **new** student in our class today.","s2c":"今天我们班来了一位新同学。"},

  {"id":192,"word":"night","phonetic":"/naɪt/","part":"n.","meaning":"夜晚，晚上","topic":"兴趣&健康情绪","level":"C",
   "s1":"She reads a book every **night** before bed.","s1c":"她每晚睡前读一本书。",
   "s2":"The stars are beautiful on a clear **night**.","s2c":"晴朗的夜晚星星非常美丽。"},

  {"id":193,"word":"no","phonetic":"/nəʊ/","part":"adv.","meaning":"不，不是","topic":"兴趣&健康情绪","level":"C",
   "s1":"**No**, I do not want any more cake, thank you.","s1c":"不，我不想再要蛋糕了，谢谢。",
   "s2":"She said **no** to the extra homework.","s2c":"她对额外的作业说了不。"},

  {"id":194,"word":"noise","phonetic":"/nɔɪz/","part":"n.","meaning":"噪音，喧闹声","topic":"兴趣&健康情绪","level":"C",
   "s1":"Please do not make a **noise** in the library.","s1c":"在图书馆请不要制造噪音。",
   "s2":"I heard a loud **noise** outside my window.","s2c":"我听到窗外有很大的噪音。"},

  {"id":195,"word":"none","phonetic":"/nʌn/","part":"pron.","meaning":"没有一个，毫无","topic":"兴趣&健康情绪","level":"C",
   "s1":"**None** of the students knew the answer.","s1c":"没有一个学生知道答案。",
   "s2":"There is **none** of the cake left.","s2c":"蛋糕一点都没有剩下了。"},

  {"id":196,"word":"nor","phonetic":"/nɔː/","part":"conj.","meaning":"也不","topic":"兴趣&健康情绪","level":"C",
   "s1":"She cannot swim, **nor** can she ride a bike.","s1c":"她不会游泳，也不会骑自行车。",
   "s2":"I do not like coffee, **nor** does my sister.","s2c":"我不喜欢咖啡，我姐姐也不喜欢。"},

  {"id":197,"word":"not","phonetic":"/nɒt/","part":"adv.","meaning":"不，没有","topic":"兴趣&健康情绪","level":"C",
   "s1":"She is **not** ready for the test yet.","s1c":"她还没有为考试做好准备。",
   "s2":"I did **not** finish my homework last night.","s2c":"我昨晚没有完成作业。"},

  {"id":198,"word":"now","phonetic":"/naʊ/","part":"adv.","meaning":"现在，此刻","topic":"兴趣&健康情绪","level":"C",
   "s1":"We are studying English **now**.","s1c":"我们现在正在学习英语。",
   "s2":"**Now** is a good time to start your revision.","s2c":"现在是开始复习的好时机。"},
]

# 统一字段格式
topic_en_map = {
  "人物性格&能力": "character",
  "校园学习&日常动作": "school",
  "日常生活&饮食购物": "daily_life",
  "出行旅游&环境天气": "travel",
  "兴趣爱好&健康情绪": "hobbies",
  "人物&状态": "states",
  "学习&工作动作": "study_work",
  "生活&饮食购物": "life_shopping",
  "出行&环境天气": "travel_weather",
  "兴趣&健康情绪": "hobbies_health",
}

result = []
for w in WORDS_DATA:
  result.append({
    "id": w["id"],
    "word": w["word"],
    "phonetic": w["phonetic"],
    "part": w["part"],
    "meaning": w["meaning"],
    "topic": w["topic"],
    "topic_en": topic_en_map.get(w["topic"], "general"),
    "level": w["level"],
    "sentence1": w["s1"],
    "sentence1_cn": w["s1c"],
    "sentence2": w.get("s2", ""),
    "sentence2_cn": w.get("s2c", ""),
  })

output = {
  "meta": {
    "total": len(result),
    "version": "1.0",
    "description": "KET高频词汇+标准例句库 四年级4个月冲刺版"
  },
  "words": result
}

import json
with open('/home/claude/ket_app/data/words.json', 'w', encoding='utf-8') as f:
  json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✓ Saved {len(result)} words")
print("Sample:", json.dumps(result[0], ensure_ascii=False))
