import streamlit as st
import requests
from datetime import datetime
import time
import random

# 页面配置 - 必须放在最前面
st.set_page_config(
    page_title="比特币价格监控",
    page_icon="₿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .price-title {
        color: white;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    .price-value {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    .change-positive {
        color: #00d26a;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .change-negative {
        color: #ff4757;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .update-time {
        color: #888;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)


def get_bitcoin_price():
    """从CoinGecko API获取比特币价格数据
    
    Returns:
        tuple: (current_price, price_change_percentage, is_mock)
               失败时返回模拟数据
    """
    try:
        # 获取 Bitcoin 的价格数据
        response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true',
            timeout=10
        )
        data = response.json()
        # 获取当前价格和24小时变化
        current_price = data['bitcoin']['usd']
        price_change_percentage = data['bitcoin']['usd_24h_change']
        return current_price, price_change_percentage, False
    except requests.exceptions.RequestException:
        # API不可达时返回模拟数据（用于演示）
        mock_price = 110000 + random.uniform(-3000, 3000)
        mock_change = random.uniform(-5.0, 5.0)
        return mock_price, mock_change, True


def format_price(price):
    """格式化价格显示"""
    return f"${price:,.2f}"


def format_percentage(change):
    """格式化百分比显示"""
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.2f}%"


def format_number(num):
    """格式化大数字显示"""
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    else:
        return f"${num:,.0f}"


# 主应用
st.title("₿ 比特币价格监控")
st.markdown("---")

# 初始化session state
if "price" not in st.session_state:
    st.session_state.price = None
if "change" not in st.session_state:
    st.session_state.change = None
if "is_mock" not in st.session_state:
    st.session_state.is_mock = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None

# 刷新按钮
if st.button("🔄 获取最新价格", use_container_width=True):
    st.session_state.price = None
    st.session_state.change = None

# 获取数据
if st.session_state.price is None:
    with st.spinner("正在获取比特币价格数据..."):
        price, change, is_mock = get_bitcoin_price()
        st.session_state.price = price
        st.session_state.change = change
        st.session_state.is_mock = is_mock
        st.session_state.last_update = datetime.now()

# 显示数据
if st.session_state.price is not None:
    price = st.session_state.price
    change = st.session_state.change
    is_mock = st.session_state.is_mock
    
    # 模拟数据警告
    if is_mock:
        st.warning("⚠️ API 不可达，当前显示为模拟数据（仅供演示）")
    
    # 价格卡片
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 20px; padding: 2rem; margin: 1rem 0; 
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            <p style="color: white; font-size: 1.2rem; margin-bottom: 0.5rem; opacity: 0.9;">
                当前价格 (USD)
            </p>
            <h1 style="color: white; font-size: 3rem; font-weight: bold; margin: 0;">
                {}
            </h1>
        </div>
    """.format(format_price(price)), unsafe_allow_html=True)
    
    # 24小时变化
    change_color = "#00d26a" if change >= 0 else "#ff4757"
    change_icon = "📈" if change >= 0 else "📉"
    
    st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 1.5rem; 
                    margin: 0.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
                    border: 1px solid #f0f0f0; text-align: center;">
            <p style="color: #666; font-size: 1rem; margin-bottom: 0.5rem;">
                24小时变化
            </p>
            <p style="color: {}; font-size: 2rem; font-weight: bold; margin: 0;">
                {} {}
            </p>
        </div>
    """.format(change_color, change_icon, format_percentage(change)), unsafe_allow_html=True)
    
    # 更新时间
    if st.session_state.last_update:
        time_str = st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"""
            <p style="color: #888; font-size: 0.9rem; text-align: center; margin-top: 2rem;">
                ⏰ 最后更新: {time_str}
            </p>
        """, unsafe_allow_html=True)

else:
    st.info("👆 点击「获取最新价格」按钮获取比特币实时价格", icon="💡")
    
    st.markdown("### 📋 关于比特币")
    st.markdown("""
        比特币（Bitcoin）是世界上第一个去中心化的加密货币，由中本聪于2008年提出，2009年正式诞生。
        
        **主要特点：**
        - 🔒 去中心化 - 不依赖任何中央机构
        - 🌐 全球流通 - 跨境转账便捷
        - 📈 有限供应 - 总量2100万枚
        - 🔍 透明公开 - 所有交易记录在区块链上
    """)

# 页脚
st.markdown("---")
data_source = "模拟数据（API不可达）" if st.session_state.get("is_mock") else "CoinGecko API"
st.markdown(f"""
    <p style="text-align: center; color: #999; font-size: 0.8rem;">
        数据来源: {data_source} | 仅供学习参考，不构成投资建议
    </p>
""", unsafe_allow_html=True)
