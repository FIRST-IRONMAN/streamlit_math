import streamlit as st
import os
import shutil
import time
from natsort import natsorted
# ======================================================================================================================


# 阿里云OSS
import oss2

access_key_id = os.getenv("OSS_ACCESS_KEY_ID")
access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET")

if access_key_id is None or access_key_secret is None:
    print("环境变量未正确设置，请检查！")
endpoint = 'oss-cn-beijing.aliyuncs.com'  # 例如：'oss-cn-hangzhou.aliyuncs.com'
bucket_name = 'handwrite-math'

# 创建 OSS 连接
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

# ======================================================================================================================
@st.cache_data
def get_anno(an_filepath):
    if not os.path.exists(an_filepath):
        anno_txt = '标注文件不存在！'
        return anno_txt
    ####

    try:
        with open(an_filepath, 'rt', encoding='utf-8') as pf:
            anno_txt = pf.read()
        ####
    except:
        anno_txt = '读标注文件失败！'
    ####

    return anno_txt


# ----------------------------------------------------------------------------------------------------------------------
@st.cache_data(ttl=3600)  # 缓存1分钟
def load_data_v1(folder_path):
    data_list = []

    # ext_tup = ('.jpg', '.png', '.jpeg')
    ext_dict = {'.jpg': 1, '.png': 1, '.jpeg': 1}

    location = folder_path
    location = os.path.abspath(location)
    for root, dirs, files in os.walk(location):
        if root != location:
            break
        ####

        loc = root

        for file in natsorted(files):
            # if not file.endswith(ext_tup):
            #     continue
            # ####

            tmp = os.path.splitext(file)
            if 2 != len(tmp):
                continue
            ####

            name_s = tmp[0]
            ext = tmp[1]

            if ext not in ext_dict:
                continue
            ####

            an_filepath = loc + '/' + name_s + '.txt'
            an_txt = get_anno(an_filepath)

            data_list.append([(loc, name_s, ext), an_txt])
        ####
    ####

    return data_list

@st.cache_data(ttl=3600)  # 缓存 1 小时
def load_data_v2(folder_path):
    data_list = []
    ext_dict = {'.jpg', '.png', '.jpeg'}  # 直接使用 set 提高查找效率

    # 1️⃣ 确保是 OSS 目录（math/set_111/ 这种格式）
    if not folder_path.startswith(("math/", "dataset/")):
        return load_data_v1(folder_path)  # 走本地文件逻辑

    # 2️⃣ 处理 OSS 逻辑 - 分页获取所有对象
    image_files = []
    txt_files = {}

    next_marker = ""
    while True:
        object_list = bucket.list_objects(prefix=folder_path, marker=next_marker, max_keys=1000)

        for obj in object_list.object_list:
            file_key = obj.key  # OSS 内部路径，例如 "math/set_111/train_001.jpg"
            file_name = os.path.basename(file_key)

            if file_name.endswith(tuple(ext_dict)):
                image_files.append((file_key, file_name))
            elif file_name.endswith('.txt'):
                txt_files[file_name] = file_key  # 记录标注文件路径

        # 继续翻页
        if object_list.is_truncated:
            next_marker = object_list.next_marker
        else:
            break  # 结束循环

    # 3️⃣ 处理图片和标注文件匹配
    for file_key, image_name in image_files:
        txt_name = os.path.splitext(image_name)[0] + '.txt'
        annotation_text = "⚠️ 无标注信息"

        if txt_name in txt_files:
            try:
                response = bucket.get_object(txt_files[txt_name])  # 直接用 OSS 内部路径读取
                annotation_text = response.read().decode('utf-8')
            except Exception as e:
                annotation_text = f"❌ 读取标注失败: {str(e)}"

        # ✅ 确保 OSS 地址拼接正确
        file_url = f"https://{bucket_name}.{endpoint}/{file_key}"

        data_list.append([(folder_path, os.path.splitext(image_name)[0], os.path.splitext(image_name)[1]), annotation_text])

    print(f"✅ 加载完成，共 {len(data_list)} 个文件")
    return data_list

# ======================================================================================================================

@st.fragment
def copy_files_v1(loc, name_s, ext, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    image_path = loc + '/' + name_s + ext
    anno_path = loc + '/' + name_s + '.txt'

    dest_image_path = dest_folder + '/' + name_s + ext
    dest_anno_path = dest_folder + '/' + name_s + '.txt'

    if os.path.exists(dest_image_path):
        return False

    shutil.copy(image_path, dest_image_path)
    if os.path.exists(anno_path):
        shutil.copy(anno_path, dest_anno_path)
    ####
    return True
# ======================================================================================================================
@st.fragment
def copy_ic_v1(loc, name_s, ext, dest_folder):
    """复制图片和文本信息到目标文件夹"""

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    ####

    counter = 0
    while True:
        if 0 == counter:
            name_s_n = name_s
        else:
            name_s_n = name_s + '_' + str(counter)
        ###

        dest_image_path = dest_folder + '/' + name_s_n + ext
        if not os.path.exists(dest_image_path):
            break
        ####

        counter += 1
    ####

    image_path = loc + '/' + name_s + ext
    shutil.copy(image_path, dest_image_path)

    anno_path = loc + '/' + name_s + '.txt'
    dest_anno_path = dest_folder + '/' + name_s_n + '.txt'
    if os.path.exists(anno_path):
        shutil.copy(anno_path, dest_anno_path)
    ####
# ======================================================================================================================
# @st.fragment
# def edit_latex_and_save(latex_text, loc, name_s, idx):
#     """
#     允许编辑 LaTeX 语法并保存到对应的 .txt 文件中。
#     """
#     # 先显示 LaTeX 公式
#     st.latex(latex_text)
#
#     # 使用 text_area 让用户编辑 LaTeX 语法，使用 idx 确保 key 唯一
#     edited_latex = st.text_area("LaTeX 语法", latex_text, height=68, key=f"latex_edit_{idx}")
#
#     # 用户点击保存按钮后，更新文件中的 LaTeX 内容
#     if st.button("修改 LaTeX", key=f"save_latex_{idx}"):
#         try:
#
#             # 将修改后的 LaTeX 内容保存到文件
#             anno_filepath = os.path.join(loc, name_s + '.txt')
#             with open(anno_filepath, 'w', encoding='utf-8') as f:
#                 f.write(edited_latex)
#
#             # 提示用户保存成功
#             st.toast("LaTeX 语法已成功更新！")
#             # 重新渲染更新后的 LaTeX
#             st.latex(edited_latex)
#         except Exception as e:
#             st.error(f"保存 LaTeX 时出错: {e}")
#     else:
#         # 如果没有修改，直接显示原始 LaTeX
#         st.latex(latex_text)

@st.fragment
def edit_latex_and_save(latex_text, loc, name_s, idx):
    """
    允许编辑 LaTeX 语法并保存到对应的 .txt 文件中。
    """
    # 创建一个占位符，用于渲染 LaTeX 公式
    latex_placeholder = st.empty()

    # 显示当前的 LaTeX 公式
    latex_placeholder.latex(latex_text)

    # 使用 text_area 让用户编辑 LaTeX 语法，使用 idx 确保 key 唯一
    edited_latex = st.text_area("编辑 LaTeX 语法", latex_text, height=68, key=f"latex_edit_{idx}")

    # 用户点击保存按钮后，更新文件中的 LaTeX 内容
    if st.button("保存修改", key=f"save_latex_{idx}"):
        try:
            # 将修改后的 LaTeX 内容保存到文件
            anno_filepath = os.path.join(loc, name_s + '.txt')
            with open(anno_filepath, 'w', encoding='utf-8') as f:
                f.write(edited_latex)

            # 提示用户保存成功
            st.toast("✅ LaTeX 语法已成功更新！")

            # 更新占位符，重新渲染更新后的 LaTeX
            latex_placeholder.latex(edited_latex)
        except Exception as e:
            st.error(f"❌ 保存 LaTeX 时出错: {e}")



# ======================================================================================================================
@st.fragment
def button_save(loc, name_s, folder_paths, idx, ext):
    # 创建并排按钮
    cols = st.columns(4)
    for col, label, dest_folder in zip(cols, ['To图像与标注Ok', 'To图像需要修改', 'To图像不需要修改', 'To其它情况'],
                                       folder_paths):
        with col:
            if st.button(f'{label}', key=f'btn_{label}_{idx}'):
                try:
                    if label == 'To图像需要修改':
                        # copy_ic(image_path, latex_text, dest_folder)
                        copy_ic_v1(loc, name_s, ext, dest_folder)
                        st.toast(f"图片已复制", icon="✅")
                    else:
                        # if copy_files(image_path, latex_text, dest_folder):
                        if copy_files_v1(loc, name_s, ext, dest_folder):
                            # st.success(f'✅ 图片已复制')
                            st.toast(f"图片已复制", icon="✅")
                        else:
                            # st.warning(f'⚠️ {label}，已存在相同文件')
                            st.toast(f'{label}，已存在相同文件', icon="⚠️")

                except Exception as e:
                    st.error(f'❌ 保存失败：{str(e)}')

# ======================================================================================================================
def main():
    """
    :return:
    """
    # time.sleep(2)
    # 设置应用程序的标题
    st.set_page_config(
        page_title='图片、标注，查看工具。',
        page_icon="🚀",
        initial_sidebar_state="expanded",
    )

    # 使用st.markdown和HTML/CSS来创建一个居中的标题
    st.markdown(
        """
        <div style="text-align: center; font-size: 2em; font-weight: bold;">
        ~图片and标注~
        </div>
        """
        , unsafe_allow_html=True
    )

    st.markdown('---')

    st.sidebar.header('📂 路径指定')

    # 文件夹选择
    folder_path = st.sidebar.text_input('文件夹路径：', placeholder='')

    st.sidebar.info('请在上面文本框输入有效路径，并按ENTER键。')
    data = load_data_v2(folder_path)
    if '' == folder_path:
        return
    ####

    # if not os.path.exists(folder_path):
    #     st.sidebar.error('文件夹路径不存在！')
    #     return
    # ####

    folder_path = os.path.abspath(folder_path)

    # 动态生成目标路径
    base_dir = os.path.dirname(folder_path)
    last_folder = os.path.basename(folder_path.rstrip(os.sep))
    output_base = os.path.join(base_dir, 'output')
    folder_paths = [
        os.path.join(output_base, f"{last_folder}_ok"),
        os.path.join(output_base, f"{last_folder}_ic"),
        os.path.join(output_base, f"{last_folder}_nic"),
        os.path.join(output_base, f"{last_folder}_other"),
    ]

    # 加载数据
    # data = load_data_v1(folder_path)
    # data = load_data_v2(folder_path)

    if 0 >= len(data):
        st.warning('当前文件夹下无有效数据！')
        return
    ####

    # 分页管理
    total_files = len(data)
    items_per_page = 100
    total_pages = (total_files + items_per_page - 1) // items_per_page
    st.sidebar.write(f'{total_files}个图像文件，分为{total_pages}页。')
    page_num = st.sidebar.number_input('当前页码：', min_value=1, max_value=total_pages, step=1, value=1)
    start_idx = (page_num - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_files)

    # 显示当前页内容
    for idx in range(start_idx, end_idx):

        (loc, name_s, ext), latex_text = data[idx]

        image_path = loc + '/' + name_s + ext
        image_path = os.path.normpath(image_path)  # 规范化路径
        # print(image_path)
        # oss_url = f"https://{bucket_name}.{endpoint}/{image_path.replace(os.sep, '/')}"
        # print(oss_url)

        # 构造 OSS 对象路径
        oss_object_key = image_path.replace(os.sep, '/')

        with st.container():
            st.caption(f'图片路径：{image_path}')

            col1, col2, col3 = st.columns([2, 4, 2])
            with col2:
                # 图片展示
                # st.image(image_path, caption=f'图片名称：{name_s}{ext}', use_container_width=True)
                st.image(oss_url, use_container_width=True)

            # 调用编辑 LaTeX 并保存的功能，传递 idx 作为唯一标识符
            edit_latex_and_save(latex_text, loc, name_s, idx)

            # 当前图片进度
            st.caption(f'当前位置：{idx + 1}/{total_files}')

            button_save(loc, name_s, folder_paths, idx, ext)

            st.markdown("---")
    st.caption(f'回到顶部：请使用快捷键 Fn + Home / Home键')


if __name__ == '__main__':
    main()

