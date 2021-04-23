#ifndef VSF_LOGGING_H
#define VSF_LOGGING_H

/* Forward delcarations */
struct mystr;
struct vsf_session;
struct vsf_sysutil_user;

extern struct vsf_session* g_session;

enum EVSFLogEntryType
{
  kVSFLogEntryNull = 1,
  kVSFLogEntryDownload,
  kVSFLogEntryUpload,
  kVSFLogEntryMkdir,
  kVSFLogEntryLogin,
  kVSFLogEntryFTPInput,
  kVSFLogEntryFTPOutput,
  kVSFLogEntryConnection,
  kVSFLogEntryDelete,
  kVSFLogEntryRename,
  kVSFLogEntryRmdir,
  kVSFLogEntryChmod,
  kVSFLogEntryDebug,
};

/* vsf_log_init()
 * PURPOSE
 * Initialize the logging services, by opening a writable file descriptor to
 * the log file (should logging be enabled).
 * PARAMETERS
 * p_sess       - the current session object
 */
void vsf_log_init(struct vsf_session* p_sess);

/* vsf_log_start_entry()
 * PURPOSE
 * Denote the start of a logged operation. Importantly, timing information
 * (if applicable) will be taken starting from this call.
 * PARAMETERS
 * p_sess       - the current session object
 * what         - the type of operation which just started
 */
void vsf_log_start_entry(struct vsf_session* p_sess,
                         enum EVSFLogEntryType what);

/* vsf_log_entry_pending()
 * PURPOSE
 * Determine whether a log entry has been started and not yet closed.
 * RETURNS
 * 0 if no log entry is pending; 1 if one is.
 */
int vsf_log_entry_pending(struct vsf_session* p_sess);

/* vsf_log_clear_entry()
 * PURPOSE
 * Clears any pending log entry.
 */
void vsf_log_clear_entry(struct vsf_session* p_sess);

/* vsf_log_do_log()
 * PURPOSE
 * Denote the end of a logged operation, specifying whether the operation
 * was successful or not.
 * PARAMETERS
 * p_sess       - the current session object
 * succeeded    - 0 for a failed operation, 1 for a successful operation
 */
void vsf_log_do_log(struct vsf_session* p_sess, int succeeded);

/* vsf_log_line()
 * PURPOSE
 * Logs a single line of information, without disturbing any pending log
 * operations (e.g. a download log spans a period of time).
 * This call must be used for any logging calls nested within a call to
 * the vsf_log_start_entry() function.
 * PARAMETERS
 * p_sess       - the current session object
 * what         - the type of operation to log
 * p_str        - the string to log
 */
void vsf_log_line(struct vsf_session* p_sess, enum EVSFLogEntryType what,
                  struct mystr* p_str);


/* log func for AceInstrument
 */
void ace_printf(const char *format, ...);


// int EQ 0
int result_check_func_1(int res);

// int NE 0
int result_check_func_2(int res);

// 0 NE vsf_sysutil_retval_is_error
int result_check_func_3(int res);

// 4399 EQ
int result_check_func_4(struct vsf_sysutil_user* res);

#endif /* VSF_LOGGING_H */

