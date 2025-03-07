import streamlit as st
import os
import shutil
import time
from natsort import natsorted
# ======================================================================================================================


# 设置应用程序的标题
# st.set_page_config(page_title='图片and标注')


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

    st.sidebar.header('路径指定')

    # 文件夹选择
    folder_path = st.sidebar.text_input('文件夹路径：', placeholder='')

    st.sidebar.info('请在上面文本框输入有效路径，并按ENTER键。')
    if '' == folder_path:
        return
    ####

    if not os.path.exists(folder_path):
        st.sidebar.error('文件夹路径不存在！')
        return
    ####

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
    data = load_data_v1(folder_path)

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

        with st.container():
            st.caption(f'图片路径：{image_path}')

            col1, col2, col3 = st.columns([2, 4, 2])
            with col2:
                # 图片展示
                # st.image(image_path, caption=f'图片名称：{name_s}{ext}', use_container_width=True)
                st.image(image_path, use_container_width=True)

            # 调用编辑 LaTeX 并保存的功能，传递 idx 作为唯一标识符
            edit_latex_and_save(latex_text, loc, name_s, idx)

            # 当前图片进度
            st.caption(f'当前位置：{idx + 1}/{total_files}')

            button_save(loc, name_s, folder_paths, idx, ext)

            st.markdown("---")
    st.caption(f'回到顶部：请使用快捷键 Fn + Home / Home键')


if __name__ == '__main__':
    main()

