import streamlit as st
import streamlit as st  # 确保导入 Streamlit 后立即调用配置函数



# ================== 饮食计划数据 ==================
diet_plan = {
    "忌口清单": {
        "禁忌食材": [
            "生姜、洋葱、辣椒、麻椒、胡椒、桂皮、八角、香叶",
            "韭菜、香菜、菠菜、茼蒿、羊肉、狗肉、鸽子肉、牛蛙、海鲜",
            "烟、酒、咖啡、茶、碳酸饮料",
            "酸性食物：葡萄、菠萝、柠檬、醋等"
        ],
        "可替代调料": ["盐", "鸡精", "生抽"]
    },
    "四周计划": {
        "第一周": {
            "早餐": {
                "周一": "小米南瓜粥（无糖） + 水煮蛋1个 + 蒸胡萝卜片",
                "周二": "燕麦牛奶（无糖燕麦+低脂牛奶） + 全麦面包1片 + 香蕉半根",
                "周三": "红枣银耳羹（银耳+红枣3颗） + 蒸山药100g + 鹌鹑蛋3个",
                "周四": "无糖豆浆300ml + 玉米半根 + 清炒西葫芦（少油）",
                "周五": "紫薯粥（紫薯50g+大米30g） + 水煮蛋1个 + 蒸西兰花",
                "周六": "糙米粥（糙米40g） + 清炒黄瓜片 + 核桃仁5颗",
                "周日": "南瓜小米糊 + 蒸芋头80g + 水煮蛋1个"
            },
            "午餐": {
                "周一": "杂粮米饭 + 清蒸鸡胸肉100g（酱油调味） + 清炒白菜",
                "周二": "白米饭1小碗 + 冬瓜排骨汤（去油） + 蒜蓉油菜（蒜炒熟）",
                "周三": "糙米饭1碗 + 香菇炖鸭肉（鸭肉去皮80g） + 水煮西蓝花胡萝卜",
                "周四": "红薯饭 + 番茄豆腐汤（番茄1/4个） + 清炒豆角",
                "周五": "白米饭1小碗 + 清蒸鲈鱼（无葱姜） + 清炒丝瓜",
                "周六": "荞麦面80g + 鸡丝黄瓜凉拌（生抽调味）",
                "周日": "杂粮饭1碗 + 莲藕炖猪肉 + 清炒莴笋"
            },
            "晚餐": {
                "周一": "青菜瘦肉粥（猪肉末30g） + 蒸南瓜100g",
                "周二": "玉米面馒头1个 + 清炒茄子（少油） + 紫菜蛋花汤",
                "周三": "小米粥1碗 + 清蒸鳕鱼100g（柠檬去腥） + 凉拌黄瓜木耳",
                "周四": "杂粮馒头1个 + 白菜豆腐煲 + 蒸胡萝卜",
                "周五": "南瓜小米粥1碗 + 蒜蓉空心菜（少油）",
                "周六": "山药排骨汤（去油） + 清炒芥蓝",
                "周日": "红豆薏米粥1碗 + 清炒西蓝花 + 蒸鸡腿（去皮）"
            }
        },
        "第二周": {
            "早餐": {
                "周一": "玉米糁粥 + 蒸红薯100g + 水煮蛋1个",
                "周二": "紫米粥 + 蒸南瓜 + 鹌鹑蛋3个",
                "周三": "无糖酸奶150ml + 全麦面包1片 + 蓝莓50g",
                "周四": "山药小米粥 + 水煮蛋1个 + 蒸胡萝卜",
                "周五": "燕麦片+牛奶煮鸡蛋（咸口） + 香蕉半根",
                "周六": "红豆粥（无糖） + 蒸芋头 + 核桃仁5颗",
                "周日": "银耳莲子羹（无糖） + 蒸山药"
            },
            "午餐": {
                "周一": "白米饭1碗 + 西芹炒百合 + 清蒸黄鱼100g（无姜）",
                "周二": "糙米饭1碗 + 芦笋炒鸡丁（鸡胸肉80g） + 番茄豆腐汤",
                "周三": "红薯饭 + 清炖牛肉（瘦牛肉100g） + 清炒油麦菜",
                "周四": "杂粮饭 + 清炒豌豆苗 + 蒸龙利鱼100g",
                "周五": "荞麦面 + 凉拌鸡丝（黄瓜） + 紫菜汤",
                "周六": "玉米饭 + 清炒娃娃菜 + 香菇蒸鸡（去骨）",
                "周日": "白米饭1碗 + 莲藕玉米排骨汤 + 蒜蓉生菜"
            },
            "晚餐": {
                "周一": "青菜豆腐汤 + 蒸紫薯100g + 水煮虾5只（可换鸡肉）",
                "周二": "小米粥 + 清炒芦笋 + 蒸蛋羹（鸡蛋1个）",
                "周三": "南瓜粥 + 清炒莴笋丝 + 香煎三文鱼（可换豆腐）",
                "周四": "杂粮馒头 + 清炒丝瓜 + 冬瓜薏仁汤",
                "周五": "燕麦牛奶粥（咸口） + 蒸胡萝卜 + 凉拌油菜",
                "周六": "山药红枣粥 + 清炒荷兰豆 + 蒸鸡胸肉",
                "周日": "红豆粥 + 清炒芥蓝 + 蒸鳕鱼"
            }
        },
        "第三周": {
            "早餐": {
                "周一": "黑米粥 + 蒸玉米段 + 水煮蛋1个",
                "周二": "核桃芝麻糊（无糖） + 蒸南瓜 + 鹌鹑蛋3个",
                "周三": "蔬菜粥（大米+胡萝卜碎） + 清炒黄瓜片",
                "周四": "紫薯牛奶羹（无糖） + 全麦面包1片",
                "周五": "小米红枣粥 + 蒸山药100g + 水煮蛋",
                "周六": "燕麦香蕉杯（无糖酸奶+燕麦片） + 杏仁10颗",
                "周日": "玉米南瓜羹 + 蒸芋头 + 水煮蛋"
            },
            "午餐": {
                "周一": "糙米饭 + 清蒸狮子头（瘦猪肉） + 上汤娃娃菜",
                "周二": "藜麦饭 + 彩椒炒鸡胸肉（彩椒非辛辣） + 清炒芦笋",
                "周三": "红薯饭 + 清炖羊肉（可用瘦牛肉替代） + 蒜蓉菜心",
                "周四": "杂粮饭 + 虾仁蒸蛋（忌海鲜可换鸡肉） + 清炒芥蓝",
                "周五": "荞麦面 + 茄汁豆腐煲（番茄1/4个） + 凉拌莴笋",
                "周六": "玉米饭 + 香菇滑鸡（去骨） + 清炒油麦菜",
                "周日": "白米饭 + 胡萝卜炖牛肉 + 清炒豌豆苗"
            },
            "晚餐": {
                "周一": "芹菜鸡肉粥 + 蒸胡萝卜块",
                "周二": "杂粮馒头 + 清炒西葫芦 + 鲫鱼豆腐汤（无姜）",
                "周三": "南瓜小米粥 + 蒜蓉茼蒿（可换油菜） + 蒸龙利鱼",
                "周四": "红豆饭 + 清炒丝瓜 + 莲藕排骨汤（去油）",
                "周五": "山药薏米粥 + 清炒芦笋 + 香煎鸡胸肉",
                "周六": "紫菜饭团（无虾皮） + 味噌豆腐汤 + 凉拌菠菜",
                "周日": "燕麦粥 + 清炒娃娃菜 + 蒸鸭肉（去皮）"
            }
        },
        "第四周": {
            "早餐": {
                "周一": "银耳枸杞羹（无糖） + 蒸紫薯100g",
                "周二": "蔬菜鸡蛋饼（西葫芦+鸡蛋） + 无糖豆浆",
                "周三": "红豆薏米粥 + 蒸南瓜 + 水煮蛋1个",
                "周四": "玉米糊 + 全麦面包1片 + 苹果片",
                "周五": "紫米莲子粥 + 蒸山药 + 鹌鹑蛋3个",
                "周六": "香蕉燕麦杯（无糖） + 核桃仁5颗",
                "周日": "南瓜小米粥 + 清炒胡萝卜丝 + 水煮蛋"
            },
            "午餐": {
                "周一": "糙米饭 + 清蒸鳕鱼（柠檬去腥） + 蒜蓉空心菜",
                "周二": "藜麦饭 + 彩椒牛柳（瘦牛肉） + 清炒芥蓝",
                "周三": "红薯饭 + 香菇炖鸡（去骨） + 上汤豆苗",
                "周四": "杂粮饭 + 清蒸鲈鱼（无姜） + 清炒莴笋丝",
                "周五": "荞麦面 + 茄汁鸡胸肉 + 凉拌木耳",
                "周六": "玉米饭 + 萝卜炖牛腩（瘦牛腩） + 清炒油菜",
                "周日": "白米饭 + 莲藕蒸肉饼（瘦猪肉） + 蒜蓉菜心"
            },
            "晚餐": {
                "周一": "青菜鸡肉粥 + 蒸芋头",
                "周二": "杂粮馒头 + 清炒芦笋 + 豆腐蛋花汤",
                "周三": "南瓜粥 + 蒜蓉西兰花 + 蒸黄鱼（无姜）",
                "周四": "红豆饭 + 清炒丝瓜 + 冬瓜排骨汤（去油）",
                "周五": "山药枸杞粥 + 清炒荷兰豆 + 香煎三文鱼",
                "周六": "紫薯粥 + 凉拌黄瓜 + 蒸鸡腿（去皮）",
                "周日": "燕麦牛奶粥 + 清炒芥蓝 + 蒸牛肉饼（瘦牛肉）"
            }
        }
    },
    "替换方案": {
        "蛋白质": ["豆腐", "鸡蛋", "去皮鸡肉", "瘦猪肉"],
        "蔬菜": ["黄瓜", "西葫芦", "娃娃菜", "芦笋", "豌豆苗"],
        "主食": ["燕麦", "藜麦", "玉米面", "糙米"]
    }
}


# ================== 自定义样式 ==================
def set_custom_style():
    st.markdown("""
    <style>
    /* 主标题样式 */
    .custom-title {
        color: #e75480;
        font-size: 2.8em !important;
        text-align: center;
        margin-bottom: 30px !important;
        font-family: 'Microsoft YaHei';
    }

    /* 侧边栏美化 */
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #fff5f5, #ffe6e6);
        padding: 25px !important;
        border-radius: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }

    /* 卡片式布局 */
    .custom-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
        transition: all 0.3s ease;
        border-left: 5px solid;
    }
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }

    /* 餐别颜色标记 */
    .breakfast { border-color: #ffb347; }
    .lunch { border-color: #77dd77; }
    .dinner { border-color: #779ecb; }

    /* 图标样式 */
    .meal-icon {
        font-size: 2em !important;
        vertical-align: middle;
        margin-right: 12px;
    }

    /* 按钮美化 */
    .stSelectbox > div > div {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ================== 主程序 ==================
def main():
    st.set_page_config(
        page_title="畅畅健康饮食计划",
        layout="wide",
        page_icon="🌸",
        initial_sidebar_state="expanded"
    )
    set_custom_style()


    # 主标题
    st.markdown('<h1 class="custom-title">🌸 畅畅专属健康饮食计划</h1>', unsafe_allow_html=True)

    # 侧边栏导航
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/100/000000/restaurant.png", width=100)
        st.header("导航菜单")
        page = st.radio("选择查看内容",
                        ["忌口清单", "四周饮食计划", "食材替换方案"],
                        index=1)

    # 页面路由
    if page == "忌口清单":
        show_restrictions()
    elif page == "四周饮食计划":
        show_diet_plan()
    else:
        show_substitutes()


# ================== 页面组件 ==================
def show_restrictions():
    st.header("🚫 严格忌口清单", divider="rainbow")
    with st.expander("📌 点击查看完整禁忌内容", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            st.subheader("❌ 禁忌食材")
            for item in diet_plan["忌口清单"]["禁忌食材"]:
                st.markdown(f"- {item}")
        with cols[1]:
            st.subheader("✅ 允许调料")
            st.markdown(" ".join([f"`{item}`" for item in diet_plan["忌口清单"]["可替代调料"]]))


def show_diet_plan():
    st.header("📆 四周饮食计划表", divider="rainbow")

    # 周选择器
    week = st.selectbox(
        "选择周数",
        ["第一周", "第二周", "第三周", "第四周"],
        index=0,
        help="请选择要查看的周计划"
    )

    plan = diet_plan["四周计划"].get(week, {})

    if plan:
        # 日期选择器
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        selected_day = st.selectbox(
            "选择日期",
            days,
            format_func=lambda x: f"📅 {x}",
            help="选择具体日期查看当日食谱"
        )

        # 食谱展示
        with st.container():
            cols = st.columns(3)

            st.markdown("""
                <style>
                    .custom-card h3 {
                        color: #ff69b4; /* 亮粉色 */
                    }
                    .custom-card p {
                        color: #ff1493; /* 深粉色 */
                    }
                </style>
            """, unsafe_allow_html=True)

            # 早餐卡片
            with cols[0]:
                st.markdown(f"""
                <div class="custom-card breakfast">
                    <h3><span class="meal-icon">🌞</span>早餐</h3>
                    <p>{plan['早餐'][selected_day]}</p>
                </div>
                """, unsafe_allow_html=True)

            # 午餐卡片
            with cols[1]:
                st.markdown(f"""
                <div class="custom-card lunch">
                    <h3><span class="meal-icon">🍱</span>午餐</h3>
                    <p>{plan['午餐'][selected_day]}</p>
                </div>
                """, unsafe_allow_html=True)

            # 晚餐卡片
            with cols[2]:
                st.markdown(f"""
                <div class="custom-card dinner">
                    <h3><span class="meal-icon">🌙</span>晚餐</h3>
                    <p>{plan['晚餐'][selected_day]}</p>
                </div>
                """, unsafe_allow_html=True)

        # 加餐推荐
        with st.expander("🍎 加餐推荐 (点击展开)", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.success("**上午加餐**")
                st.markdown("- 苹果 1个 (约150g)")
                st.markdown("- 梨 1个 (去皮切块)")
            with col2:
                st.success("**下午加餐**")
                st.markdown("- 猕猴桃 1个 + 杏仁8颗")
                st.markdown("- 木瓜 100g + 核桃仁5颗")

        # 营养提示
        st.info("""
        💡 **营养小贴士**  
        - 每日蔬菜摄入 ≥500g  
        - 饮水量 1500-2000ml  
        - 坚果摄入 ≤20g/天
        """)


def show_substitutes():
    st.header("🔄 食材替换方案", divider="rainbow")

    # 蛋白质替换
    with st.expander("🥚 蛋白质替换方案", expanded=True):
        st.markdown("""
        ```python
        ["豆腐", "鸡蛋", "去皮鸡肉", "瘦猪肉"]
        """)
        st.write("👉 海鲜过敏者可选择豆腐/鸡肉替代鱼类")

    # 蔬菜替换
    with st.expander("🥦 蔬菜替换方案"):
        st.markdown("""
        ```python
        ["黄瓜", "西葫芦", "娃娃菜", "芦笋", "豌豆苗"]
        """)
        st.write("👉 避免使用韭菜/香菜/茼蒿")

    # 主食替换
    with st.expander("🍚 主食替换方案"):
        st.markdown("""
        ```python
        ["燕麦", "藜麦", "玉米面", "糙米"]
        """)
        st.write("👉 建议粗细粮搭配食用")

    # 烹饪贴士
    st.markdown("---")
    st.subheader("👩‍🍳 烹饪注意事项")
    st.write("""
    1. 使用葱/柠檬汁去腥代替生姜  
    2. 每日食用油 ≤25g（优选橄榄油）  
    3. 避免使用复合调味料  
    4. 肉类烹饪前需去皮去脂
    """)


if __name__ == "__main__":
    main()