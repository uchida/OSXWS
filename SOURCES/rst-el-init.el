;;
;; rst-el-init.el
;;
;;      for Vine Linux with emacsen-common
;;      IWAI, Masaharu <iwai@alib.jp>

(defcustom vine-default-rst-el t
  "A boolean for vine-default-rst-el"
  :type 'boolean)

(add-hook 'vine-default-setup-hook
          (lambda()
            (if vine-default-rst-el
                (require 'vine-default-rst-el))))

;;; end of file
