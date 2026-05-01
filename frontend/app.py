import streamlit as st
import requests
import re
from api_client import get_notes, add_note, update_note, delete_note, signup, login, google_login, resend_verification

st.set_page_config(page_title="Note App", page_icon="📝")

if "user" not in st.session_state:
    st.session_state.user = None
if "notes" not in st.session_state:
    st.session_state.notes = []
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "show_login" not in st.session_state:
    st.session_state.show_login = True

def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@gmail\.com$", re.IGNORECASE)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))

def handle_google_login_callback():
    params = st.query_params
    raw_token = params.get("id_token")
    if raw_token:
        id_token = raw_token[0] if isinstance(raw_token, list) else raw_token
        try:
            user = google_login(id_token)
            st.session_state.user = user
            st.session_state.notes = get_notes(user["idToken"])
            clear_google_query_params()
            st.success("Đăng nhập Google thành công")
            st.rerun()
        except requests.HTTPError as e:
            st.error(f"Đăng nhập Google thất bại: {e}")
            clear_google_query_params()
        except Exception as e:
            st.error(f"Lỗi xử lý Google login: {e}")
            clear_google_query_params()

handle_google_login_callback()

st.title("Note App")

def login_form():
    st.subheader("Đăng nhập")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập")
        goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký")
    if goto_signup:
        st.session_state.show_signup = True
        st.session_state.show_login = False
        st.rerun()
    if submitted:
        # Client-side validation
        email = email.strip()
        if not email or not password.strip():
            st.warning("Vui lòng nhập email và mật khẩu.")
            return
        if not is_valid_email(email):
            st.warning("Email không hợp lệ.")
            return
        try:
            user = login(email, password)
            st.session_state.user = user
            st.session_state.notes = get_notes(user["idToken"])
            st.success("Đăng nhập thành công")
            st.rerun()
        except requests.HTTPError as e:
            code = None
            detail_text = None
            if hasattr(e, 'response') and e.response is not None:
                try:
                    code = e.response.status_code
                except Exception:
                    code = None
                try:
                    detail_text = e.response.json().get("detail")
                except Exception:
                    try:
                        detail_text = e.response.text
                    except Exception:
                        detail_text = None
            if not detail_text:
                detail_text = "Đăng nhập thất bại"
            # remove leading HTTP status codes or verbose prefixes like "409: " or "409 Client Error: "
            try:
                if isinstance(detail_text, str):
                    detail_text = re.sub(r"^\s*(?:\d{3}\s*[:\-]\s*|(?:\d{3}\s+)?Client Error[:\-]?\s*)", "", detail_text, flags=re.IGNORECASE)
            except Exception:
                pass
            if code == 401:
                st.error("Email hoặc mật khẩu không đúng.")
            elif code == 403:
                st.error("Email chưa được xác thực. Vui lòng kiểm tra email và xác nhận.")
                if st.button("Gửi lại email xác thực"):
                    try:
                        resp = resend_verification(email)
                        link = resp.get("link")
                        if link:
                            st.success("Đã tạo link xác thực. Mở link để xác thực tài khoản.")
                            st.markdown(f"[Mở link xác thực]({link})", unsafe_allow_html=True)
                        else:
                            st.success("Đã gửi email xác thực (nếu được hỗ trợ).")
                    except requests.HTTPError as e:
                        # show response message if possible
                        msg = None
                        if hasattr(e, 'response') and e.response is not None:
                            try:
                                msg = e.response.json().get('detail')
                            except Exception:
                                msg = e.response.text
                        st.error(f"Gửi lại email xác thực thất bại: {msg or str(e)}")
                    except Exception as e:
                        st.error(f"Lỗi khi gửi lại email xác thực: {e}")
            else:
                st.error(f"Đăng nhập thất bại: {detail_text}")
        except Exception as e:
            st.error(f"Lỗi đăng nhập: {e}")
    st.markdown("### Hoặc")
    # Luôn trỏ tới backend /auth/google/start
    google_login_url = "http://localhost:8000/auth/google/start"
    st.markdown(
        f'''
        <a href="{google_login_url}" target="_self" style="
            display: inline-block;
            width: 100%;
            text-align: center;
            padding: 0.6rem 1rem;
            background-color: white;
            color: black;
            text-decoration: none;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
            font-weight: 600;
        ">
            Đăng nhập với Google
        </a>
        ''',
        unsafe_allow_html=True,
    )

def signup_form():
    st.subheader("Đăng ký")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Tạo tài khoản")
        goto_login = st.form_submit_button("Đã có tài khoản? Đăng nhập")
    if goto_login:
        st.session_state.show_signup = False
        st.session_state.show_login = True
        st.rerun()
    if submitted:
        # Client-side validation
        email = email.strip()
        if not email or not password.strip():
            st.warning("Vui lòng nhập email và mật khẩu.")
            return
        if not is_valid_email(email):
            st.warning("Email không hợp lệ.")
            return
        if len(password) < 6:
            st.warning("Mật khẩu phải có ít nhất 6 ký tự.")
            return
        try:
            signup(email, password)
            st.success("Tạo tài khoản thành công, hãy đăng nhập")
            st.session_state.show_signup = False
            st.session_state.show_login = True
            st.rerun()
        except requests.HTTPError as e:
            code = None
            detail_text = None
            if hasattr(e, 'response') and e.response is not None:
                try:
                    code = e.response.status_code
                except Exception:
                    code = None
                try:
                    detail_text = e.response.json().get("detail")
                except Exception:
                    try:
                        detail_text = e.response.text
                    except Exception:
                        detail_text = None
            if not detail_text:
                detail_text = "Đăng ký thất bại"
            try:
                if isinstance(detail_text, str):
                    detail_text = re.sub(r"^\s*(?:\d{3}\s*[:\-]\s*|(?:\d{3}\s+)?Client Error[:\-]?\s*)", "", detail_text, flags=re.IGNORECASE)
            except Exception:
                pass
            st.error(f"Đăng ký thất bại: {detail_text}")
        except Exception as e:
            st.error(f"Lỗi đăng ký: {e}")

if st.session_state.user:
    st.success(f"Đang đăng nhập: {st.session_state.user['email']}")
    if st.button("Đăng xuất"):
        st.session_state.user = None
        st.session_state.notes = []
        clear_google_query_params()
        st.rerun()
    if st.button("Tải lại danh sách ghi chú"):
        st.session_state.notes = get_notes(st.session_state.user["idToken"])
    st.subheader("Danh sách ghi chú")
    if "editing_note" not in st.session_state:
        st.session_state.editing_note = None
    for note in st.session_state.notes:
        with st.container():
            st.markdown(f"### 📝 {note['title']}")
            st.write(note["content"])
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Sửa", key=f"edit_{note['id']}"):
                    st.session_state.editing_note = note["id"]
                    st.session_state[f"edit_title_{note['id']}"] = note["title"]
                    st.session_state[f"edit_content_{note['id']}"] = note["content"]
                    st.rerun()
            with col2:
                if st.button(f"Xóa", key=f"del_{note['id']}"):
                    st.session_state[f"confirm_delete_{note['id']}"] = True
            # Xác nhận xóa
            if st.session_state.get(f"confirm_delete_{note['id']}", False):
                st.warning("Bạn có chắc chắn muốn xóa ghi chú này không?")
                confirm, cancel = st.columns([1, 1])
                with confirm:
                    if st.button("Xác nhận xóa", key=f"confirm_{note['id']}"):
                        delete_note(st.session_state.user["idToken"], note["id"])
                        st.session_state.notes = get_notes(st.session_state.user["idToken"])
                        st.success("Đã xóa ghi chú!")
                        st.session_state[f"confirm_delete_{note['id']}"] = False
                        st.rerun()
                with cancel:
                    if st.button("Hủy xóa", key=f"cancel_del_{note['id']}"):
                        st.session_state[f"confirm_delete_{note['id']}"] = False
                        st.info("Đã hủy xóa ghi chú.")
                        st.rerun()
            # Form sửa
            if st.session_state.editing_note == note["id"]:
                st.info("**Chỉnh sửa ghi chú**")
                new_title = st.text_input("Tiêu đề mới", value=st.session_state.get(f"edit_title_{note['id']}", note["title"]), key=f"edit_title_{note['id']}")
                new_content = st.text_area("Nội dung mới", value=st.session_state.get(f"edit_content_{note['id']}", note["content"]), key=f"edit_content_{note['id']}")
                save, cancel = st.columns([1, 1])
                with save:
                    if st.button("Lưu", key=f"save_{note['id']}"):
                        if not new_title.strip() or not new_content.strip():
                            st.warning("Tiêu đề và nội dung không được để trống.")
                        else:
                            update_note(st.session_state.user["idToken"], note["id"], new_title.strip(), new_content.strip())
                            st.session_state.notes = get_notes(st.session_state.user["idToken"])
                            st.success("Đã cập nhật ghi chú!")
                            st.session_state.editing_note = None
                            st.rerun()
                with cancel:
                    if st.button("Hủy", key=f"cancel_{note['id']}"):
                        st.session_state.editing_note = None
                        st.info("Đã hủy chỉnh sửa.")
                        st.rerun()
    st.subheader("Thêm ghi chú mới")
    title = st.text_input("Tiêu đề")
    content = st.text_area("Nội dung")
    if st.button("Thêm ghi chú"):
        if not title.strip() or not content.strip():
            st.warning("Vui lòng nhập đầy đủ tiêu đề và nội dung trước khi thêm ghi chú.")
        else:
            add_note(st.session_state.user["idToken"], title.strip(), content.strip())
            st.session_state.notes = get_notes(st.session_state.user["idToken"])
            st.success("Đã thêm ghi chú!")
else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()